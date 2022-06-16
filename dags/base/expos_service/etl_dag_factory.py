import json
from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from bson.objectid import ObjectId

from base.expos_service.clean_data_taskgroup import CleanDataTaskGroup
from base.expos_service.download_csvs_from_s3_taskgroup import DownloadCsvsFromS3TaskGroup
from base.expos_service.load_missing_hierarchy_from_s3_taskgroup import LoadMissingHierarchyFromS3TaskGroup
from base.utils.conditional_operator import conditional_operator
from base.utils.load_csv_into_temp_tables_taskgroup import LoadCsvIntoTempTablesTaskGroup
from base.expos_service.send_broken_hierarchy_data import send_broken_hierarchy_data
from base.utils.tables_insert_taskgroup import TableOperationsTaskGroup
from base.expos_service.extract_docdb_csv_taskgroup import \
    ExtractDocumentDbCsvTaskGroup
from base.expos_service.extract_pg_csv_taskgroup import \
    ExtractPostgresCsvTaskGroup
from base.expos_service.health_checks_taskgroup import HealthChecksTaskGroup
from base.expos_service.upload_csvs_to_s3_taskgroup import UploadCsvsToS3TaskGroup
from base.utils.mongo import execute_query
from base.utils.slack import notify_start_task
from base.utils.table_names import TableNameManager
from base.utils.tunneler import Tunneler
from config.common.defaults import default_task_kwargs, default_dag_kwargs
from config.common.settings import SHOULD_UPLOAD_TO_S3
from config.expos_service.settings import (
    ES_AIRFLOW_DATABASE_CONN_ID,
    ES_ETL_DAG_ID,
    ES_ETL_DAG_SCHEDULE_INTERVAL,
    ES_ETL_DAG_START_DATE_VALUE,
    ES_REMOTE_MONGO_HOST,
    ES_REMOTE_MONGO_PORT,
    ES_EMBONOR_MONGO_CONN_ID,
    ES_EMBONOR_MONGO_DB_NAME,
    ES_REMOTE_RDS_HOST,
    ES_REMOTE_RDS_PORT,
    IS_LOCAL_RUN,
    ES_MONGO_COLLECTIONS_TO_EXTRACT,
    ES_PG_TABLES_TO_EXTRACT,
    ES_ETL_CONFORM_OPERATIONS_ORDER, ES_ETL_STAGED_OPERATIONS_ORDER, ES_ETL_TARGET_OPERATIONS_ORDER,
    ES_FETCH_OLD_EVALUATIONS_KEY, ES_ETL_CHECK_RUN_DAG_ID, ES_ETL_CHECK_RUN_DAG_SCHEDULE_INTERVAL,
    ES_ETL_POSTPROCESSING_OPERATIONS_ORDER,
)

from operators.postgres.create_job import PostgresOperatorCreateJob


class EtlDagFactory:
    def __init__(self, check_run=False):
        self.check_run = check_run
        self.dag_id = ES_ETL_CHECK_RUN_DAG_ID if check_run else ES_ETL_DAG_ID
        self.schedule_interval = ES_ETL_CHECK_RUN_DAG_SCHEDULE_INTERVAL if check_run else ES_ETL_DAG_SCHEDULE_INTERVAL

    def build(self) -> DAG:
        _start_date = datetime.strptime(
            ES_ETL_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
            'retries': 2,
            'retry_delay': timedelta(seconds=5),
        }
        _pg_table_list = ES_PG_TABLES_TO_EXTRACT
        _mongo_collection_list = ES_MONGO_COLLECTIONS_TO_EXTRACT
        _tables_to_insert = _pg_table_list + _mongo_collection_list
        _conform_operations = ES_ETL_CONFORM_OPERATIONS_ORDER
        _staged_operations = ES_ETL_STAGED_OPERATIONS_ORDER
        _target_operations = ES_ETL_TARGET_OPERATIONS_ORDER
        _postprocessing_operations = ES_ETL_POSTPROCESSING_OPERATIONS_ORDER
        _table_manager = TableNameManager(_tables_to_insert)

        pg_tunnel = Tunneler(
            ES_REMOTE_RDS_PORT, ES_REMOTE_RDS_HOST, 5433) if IS_LOCAL_RUN else None
        mongo_tunnel = Tunneler(
            ES_REMOTE_MONGO_PORT, ES_REMOTE_MONGO_HOST, 27018) if IS_LOCAL_RUN else None

        with DAG(
                self.dag_id,
                **default_dag_kwargs,
                schedule_interval=self.schedule_interval,
                default_args=_default_args,
                user_defined_filters={
                    'oid_from_dict': lambda dict: dict[0]['_id']['$oid'],
                    'from_json': lambda jsonstr: json.loads(jsonstr),
                    'object_ids_from_array': lambda arr: list(map(lambda record: ObjectId(record['_id']['$oid']), arr)),
                },
                render_template_as_native_obj=True,
        ) as _dag:
            create_job_task = PostgresOperatorCreateJob(
                task_id='create_job',
                sql='insert_job.sql',
                dag=_dag,
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            )

            _job_id = PostgresOperatorCreateJob.get_job_id(_dag.dag_id, create_job_task.task_id)

            notify_etl_start = notify_start_task(_dag)

            _survey_filters = {'name': 'Autoevaluación'}
            _fetch_old_surveys = Variable.get(ES_FETCH_OLD_EVALUATIONS_KEY) == 'True'

            if not _fetch_old_surveys:
                _survey_filters['paused'] = False

            health_checks_task = conditional_operator(
                dag=_dag,
                group_id='health_checks',
                pg_tunnel=pg_tunnel,
                operator=HealthChecksTaskGroup,
                condition=SHOULD_UPLOAD_TO_S3 or self.check_run,
                should_build=True,
            )

            get_self_evaluation_survey_id = conditional_operator(
                operator=PythonOperator,
                condition=SHOULD_UPLOAD_TO_S3 or self.check_run,
                task_id='get_self_evaluation_survey_id',
                python_callable=execute_query,
                do_xcom_push=True,
                op_kwargs={
                    'collection_name': 'surveys',
                    'conn_id': ES_EMBONOR_MONGO_CONN_ID,
                    'db_name': ES_EMBONOR_MONGO_DB_NAME,
                    'filters': _survey_filters,
                    'tunnel': mongo_tunnel,
                },
            )

            upload_csvs_to_s3 = conditional_operator(
                condition=SHOULD_UPLOAD_TO_S3 and not self.check_run,
                operator=UploadCsvsToS3TaskGroup,
                dag=_dag,
                group_id='upload_csvs_to_s3',
                file_names=_pg_table_list + _mongo_collection_list,
                should_build=True,
            )

            extract_from_pg = conditional_operator(
                dag=_dag,
                group_id='extract_from_pg',
                pg_tunnel=pg_tunnel,
                table_list=_pg_table_list,
                should_build=True,
                condition=SHOULD_UPLOAD_TO_S3 or self.check_run,
                operator=ExtractPostgresCsvTaskGroup,
            )

            extract_from_mongo = conditional_operator(
                dag=_dag,
                operator=ExtractDocumentDbCsvTaskGroup,
                condition=SHOULD_UPLOAD_TO_S3 or self.check_run,
                should_build=True,
                group_id='extract_from_document_db',
                mongo_tunnel=mongo_tunnel,
                collection_list=_mongo_collection_list,
            )

            download_csvs_from_s3 = conditional_operator(
                dag=_dag,
                operator=DownloadCsvsFromS3TaskGroup,
                condition=not SHOULD_UPLOAD_TO_S3 and not self.check_run,
                group_id='download_csvs_from_s3',
                should_build=True,
                file_names=_pg_table_list + _mongo_collection_list,
            )

            load_missing_hierarchy_from_s3 = LoadMissingHierarchyFromS3TaskGroup(
                group_id='load_missing_hierarchy_from_s3',
                dag=_dag,
            ).build()

            load_into_tmp_tables = LoadCsvIntoTempTablesTaskGroup(
                tables_to_insert=_tables_to_insert,
                task_group_id='create_and_load_tmp_tables_from_csv',
                sql_folder='expos_service',
                check_run=self.check_run,
            ).build()

            raw_tables_insert = TableOperationsTaskGroup(
                table_list=_table_manager.get_normalized_names(),
                sql_folder='expos_service',
                stage='raw',
                job_id=_job_id,
            ).build()

            typed_tables_insert = TableOperationsTaskGroup(
                table_list=_table_manager.get_normalized_names(),
                sql_folder='expos_service',
                stage='typed',
                job_id=_job_id,
            ).build()

            conform_tables_insert = TableOperationsTaskGroup(
                table_list=_conform_operations,
                sql_folder='expos_service',
                stage='conform',
                sequential=True,
                job_id=_job_id,
            ).build()

            staged_tables_insert = TableOperationsTaskGroup(
                table_list=_staged_operations,
                sql_folder='expos_service',
                stage='staged',
                sequential=True,
                job_id=_job_id,
            ).build()

            target_tables_insert = DummyOperator(task_id='dummy_target_inserts') if self.check_run \
                else TableOperationsTaskGroup(
                table_list=_target_operations,
                sql_folder='expos_service',
                stage='target',
                sequential=True,
                job_id=_job_id,
            ).build()

            postprocessing_tables = TableOperationsTaskGroup(
                table_list=_postprocessing_operations,
                sql_folder='expos_service',
                stage='postprocessing',
                sequential=True,
                job_id=_job_id,
            ).build()

            process_old_evaluations_data = conditional_operator(
                task_id='process_old_evaluations_data',
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                sql="""
                                VACUUM ANALYZE answer;
                                CALL process_old_survey_data();
                            """,
                operator=PostgresOperator,
                condition=_fetch_old_surveys,
            )

            precalculate_answers = PostgresOperator(
                task_id='precalculate_answers',
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                sql="""
                    REFRESH MATERIALIZED VIEW CONCURRENTLY preprocessed_answers;
                """,
            )

            report_broken_hierarchy = PythonOperator(
                task_id='report_broken_hierarchy',
                python_callable=send_broken_hierarchy_data,
                op_args=[_job_id],
            )

            clean_data = CleanDataTaskGroup(
                stage='cleanup',
                job_id=_job_id,
            ).build()

            notify_etl_start >> create_job_task >> load_missing_hierarchy_from_s3 >> health_checks_task >> \
                get_self_evaluation_survey_id >> [extract_from_pg, extract_from_mongo] >> upload_csvs_to_s3 >> \
                download_csvs_from_s3 >> load_into_tmp_tables >> raw_tables_insert >> typed_tables_insert >>\
                conform_tables_insert >> staged_tables_insert >> target_tables_insert >> postprocessing_tables >>\
                precalculate_answers >> report_broken_hierarchy >> clean_data >> process_old_evaluations_data

        return _dag
