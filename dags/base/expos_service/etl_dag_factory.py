import json
from datetime import datetime, timedelta

from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from base.expos_service.clean_data_taskgroup import CleanDataTaskGroup
from base.expos_service.download_csvs_from_s3_taskgroup import DownloadCsvsFromS3TaskGroup
from base.utils.load_csv_into_temp_tables_taskgroup import LoadCsvIntoTempTablesTaskGroup
from base.expos_service.send_broken_hierarchy_data import send_broken_hierarchy_data
from base.utils.tables_insert_taskgroup import TablesInsertTaskGroup
from base.expos_service.extract_docdb_csv_taskgroup import \
    ExtractDocumentDbCsvTaskGroup
from base.expos_service.extract_pg_csv_taskgroup import \
    ExtractPostgresCsvTaskGroup
from base.expos_service.health_checks_taskgroup import HealthChecksTaskGroup
from base.expos_service.upload_csvs_to_s3_taskgroup import UploadCsvsToS3TaskGroup
from base.utils.mongo import execute_query
from base.utils.slack import build_status_msg, send_slack_notification
from base.utils.table_names import TableNameManager
from base.utils.tunneler import Tunneler
from config.common.settings import SHOULD_NOTIFY, SHOULD_UPLOAD_TO_S3
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
    ES_REMOTE_RDS_PORT, ES_SQL_PATH,
    IS_LOCAL_RUN,
    ES_MONGO_COLLECTIONS_TO_EXTRACT,
    ES_PG_TABLES_TO_EXTRACT,
    ES_ETL_CONFORM_OPERATIONS_ORDER, ES_ETL_STAGED_OPERATIONS_ORDER, ES_ETL_TARGET_OPERATIONS_ORDER,
    ES_FETCH_OLD_EVALUATIONS_KEY,
)

from operators.postgres.create_job import PostgresOperatorCreateJob


class EtlDagFactory:

    @staticmethod
    def on_failure_callback(context):
        if not SHOULD_NOTIFY:
            return
        ti = context['task_instance']
        run_id = context['run_id']
        send_slack_notification(notification_type='alert',
                                payload=build_status_msg(
                                    dag_id=ES_ETL_DAG_ID,
                                    status='failed',
                                    mappings={'run_id': run_id, 'task_id': ti.task_id},
                                ))

    @staticmethod
    def on_success_callback(context):
        if not SHOULD_NOTIFY:
            return

        run_id = context['run_id']
        send_slack_notification(notification_type='success',
                                payload=build_status_msg(
                                    dag_id=ES_ETL_DAG_ID,
                                    status='finished',
                                    mappings={'run_id': run_id},
                                ))

    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            ES_ETL_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(seconds=240),
            'retries': 2,
            'retry_delay': timedelta(seconds=5),
            'on_failure_callback': EtlDagFactory.on_failure_callback,
        }
        _pg_table_list = ES_PG_TABLES_TO_EXTRACT
        _mongo_collection_list = ES_MONGO_COLLECTIONS_TO_EXTRACT
        _tables_to_insert = _pg_table_list + _mongo_collection_list
        _conform_operations = ES_ETL_CONFORM_OPERATIONS_ORDER
        _staged_operations = ES_ETL_STAGED_OPERATIONS_ORDER
        _target_operations = ES_ETL_TARGET_OPERATIONS_ORDER
        _table_manager = TableNameManager(_tables_to_insert)
        pg_tunnel = Tunneler(
            ES_REMOTE_RDS_PORT, ES_REMOTE_RDS_HOST, 5433) if IS_LOCAL_RUN else None
        mongo_tunnel = Tunneler(
            ES_REMOTE_MONGO_PORT, ES_REMOTE_MONGO_HOST, 27018) if IS_LOCAL_RUN else None

        with DAG(
                ES_ETL_DAG_ID,
                schedule_interval=ES_ETL_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                template_searchpath=ES_SQL_PATH,
                max_active_runs=1,
                on_success_callback=EtlDagFactory.on_success_callback,
                catchup=False,
                user_defined_filters={
                    'oid_from_dict': lambda dict: dict[0]['_id']['$oid'],
                    'from_json': lambda jsonstr: json.loads(jsonstr),
                },
        ) as _dag:
            create_job_task = PostgresOperatorCreateJob(
                task_id='create_job',
                sql='insert_job.sql',
                dag=_dag,
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            )

            _job_id = PostgresOperatorCreateJob.get_job_id(_dag.dag_id, create_job_task.task_id)
            if SHOULD_NOTIFY:
                notify_etl_start = PythonOperator(
                    task_id='notify_etl_start',
                    op_kwargs={
                        'payload': build_status_msg(
                            dag_id=ES_ETL_DAG_ID,
                            status='started',
                            mappings={'run_id': '{{ run_id }}'},
                        ),
                        'notification_type': 'success'},
                    python_callable=send_slack_notification,
                    dag=_dag,
                )

            _survey_filters = {'name': 'Autoevaluación'}
            _fetch_old_surveys = Variable.get(ES_FETCH_OLD_EVALUATIONS_KEY) == 'True'

            if not _fetch_old_surveys:
                _survey_filters['paused'] = False

            if SHOULD_UPLOAD_TO_S3:
                health_checks_task = HealthChecksTaskGroup(
                    _dag, group_id='health_checks', pg_tunnel=pg_tunnel).build()

                get_self_evaluation_survey_id = PythonOperator(
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

                upload_csvs_to_s3 = UploadCsvsToS3TaskGroup(
                    _dag,
                    group_id='upload_csvs_to_s3',
                    file_names=_pg_table_list + _mongo_collection_list,
                ).build()
                extract_from_pg = ExtractPostgresCsvTaskGroup(
                    _dag, group_id='extract_from_pg', pg_tunnel=pg_tunnel, table_list=_pg_table_list).build()

                extract_from_mongo = ExtractDocumentDbCsvTaskGroup(
                    _dag,
                    group_id='extract_from_document_db',
                    mongo_tunnel=mongo_tunnel,
                    collection_list=_mongo_collection_list,
                ).build()
            else:
                download_csvs_from_s3 = DownloadCsvsFromS3TaskGroup(
                    _dag,
                    group_id='download_csvs_from_s3',
                    file_names=_pg_table_list + _mongo_collection_list,
                ).build()

            load_into_tmp_tables = LoadCsvIntoTempTablesTaskGroup(
                tables_to_insert=_tables_to_insert,
                task_group_id='create_and_load_tmp_tables_from_csv',
                sql_folder='expos_service',
            ).build()

            raw_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_table_manager.get_normalized_names(),
                sql_folder='expos_service',
                stage='raw',
                job_id=_job_id,
            ).build()

            typed_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_table_manager.get_normalized_names(),
                sql_folder='expos_service',
                stage='typed',
                job_id=_job_id,
            ).build()

            conform_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_conform_operations,
                sql_folder='expos_service',
                stage='conform',
                sequential=True,
                job_id=_job_id,
            ).build()

            staged_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_staged_operations,
                sql_folder='expos_service',
                stage='staged',
                sequential=True,
                job_id=_job_id,
            ).build()

            target_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_target_operations,
                sql_folder='expos_service',
                stage='target',
                sequential=True,
                job_id=_job_id,
            ).build()

            if _fetch_old_surveys:
                process_old_evaluations_data = PostgresOperator(
                    task_id='process_old_evaluations_data',
                    postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                    sql="""
                        VACUUM ANALYZE answer;
                        CALL process_old_survey_data();
                    """,
                )

            precalculate_answers = PostgresOperator(
                task_id='precalculate_answers',
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                sql="""
                    CALL calculate_answer_based_data();
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

            if SHOULD_NOTIFY:
                notify_etl_start >> create_job_task

            if SHOULD_UPLOAD_TO_S3:
                create_job_task >> health_checks_task >> get_self_evaluation_survey_id >> \
                    [extract_from_pg, extract_from_mongo] >>\
                    upload_csvs_to_s3 >> load_into_tmp_tables
            else:
                create_job_task >> download_csvs_from_s3 >> load_into_tmp_tables

            load_into_tmp_tables >> raw_tables_insert >> typed_tables_insert >> conform_tables_insert >>\
                staged_tables_insert >> target_tables_insert >>\
                precalculate_answers >> report_broken_hierarchy >> clean_data

            if _fetch_old_surveys:
                clean_data >> process_old_evaluations_data
        return _dag
