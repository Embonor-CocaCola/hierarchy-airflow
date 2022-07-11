import json
from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator

from hierarchy_service.base.etl.clean_data_taskgroup import CleanDataTaskGroup
from hierarchy_service.base.etl.load_missing_hierarchy_from_s3_taskgroup import LoadMissingHierarchyFromS3TaskGroup
from hierarchy_service.base.utils.load_csv_into_temp_tables_taskgroup import LoadCsvIntoTempTablesTaskGroup
from hierarchy_service.base.etl.send_broken_hierarchy_data import send_broken_hierarchy_data
from hierarchy_service.base.utils.tables_insert_taskgroup import TableOperationsTaskGroup
from hierarchy_service.base.etl.extract_pg_csv_taskgroup import \
    ExtractPostgresCsvTaskGroup
from hierarchy_service.base.utils.slack import notify_start_task
from hierarchy_service.base.utils.table_names import TableNameManager
from hierarchy_service.base.utils.tunneler import Tunneler
from hierarchy_service.config.common.defaults import default_task_kwargs, default_dag_kwargs
from hierarchy_service.config.common.settings import SHOULD_USE_TUNNEL
from hierarchy_service.config.etl.settings import (
    HIERARCHY_AIRFLOW_DATABASE_CONN_ID,
    HIERARCHY_ETL_DAG_ID,
    HIERARCHY_ETL_DAG_SCHEDULE_INTERVAL,
    HIERARCHY_ETL_DAG_START_DATE_VALUE,
    HIERARCHY_REMOTE_RDS_HOST,
    HIERARCHY_REMOTE_RDS_PORT,
    HIERARCHY_PG_TABLES_TO_EXTRACT,
    HIERARCHY_ETL_CONFORM_OPERATIONS_ORDER, HIERARCHY_ETL_STAGED_OPERATIONS_ORDER,
    HIERARCHY_ETL_TARGET_OPERATIONS_ORDER,
    HIERARCHY_ETL_POSTPROCESSING_OPERATIONS_ORDER,
)

from operators.postgres.create_job import PostgresOperatorCreateJob


class EtlDagFactory:
    def __init__(self):
        self.dag_id = HIERARCHY_ETL_DAG_ID
        self.schedule_interval = HIERARCHY_ETL_DAG_SCHEDULE_INTERVAL

    def build(self) -> DAG:
        _start_date = datetime.strptime(
            HIERARCHY_ETL_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
            'retries': 2,
            'retry_delay': timedelta(seconds=5),
        }
        _pg_table_list = HIERARCHY_PG_TABLES_TO_EXTRACT
        _tables_to_insert = _pg_table_list
        _conform_operations = HIERARCHY_ETL_CONFORM_OPERATIONS_ORDER
        _staged_operations = HIERARCHY_ETL_STAGED_OPERATIONS_ORDER
        _target_operations = HIERARCHY_ETL_TARGET_OPERATIONS_ORDER
        _postprocessing_operations = HIERARCHY_ETL_POSTPROCESSING_OPERATIONS_ORDER
        _table_manager = TableNameManager(_tables_to_insert)

        pg_tunnel = Tunneler(
            HIERARCHY_REMOTE_RDS_PORT, HIERARCHY_REMOTE_RDS_HOST, 5433) if SHOULD_USE_TUNNEL else None

        with DAG(
                self.dag_id,
                **default_dag_kwargs,
                schedule_interval=self.schedule_interval,
                default_args=_default_args,
                user_defined_filters={
                    'from_json': lambda jsonstr: json.loads(jsonstr),
                },
                render_template_as_native_obj=True,
        ) as _dag:
            create_job_task = PostgresOperatorCreateJob(
                task_id='create_job',
                sql='insert_job.sql',
                dag=_dag,
                postgres_conn_id=HIERARCHY_AIRFLOW_DATABASE_CONN_ID,
            )

            _job_id = PostgresOperatorCreateJob.get_job_id(_dag.dag_id, create_job_task.task_id)

            notify_etl_start = notify_start_task(_dag)

            extract_from_pg = ExtractPostgresCsvTaskGroup(
                dag=_dag,
                group_id='extract_from_pg',
                pg_tunnel=pg_tunnel,
                table_list=_pg_table_list,
            ).build()

            load_missing_hierarchy_from_s3 = LoadMissingHierarchyFromS3TaskGroup(
                group_id='load_missing_hierarchy_from_s3',
                dag=_dag,
            ).build()

            load_into_tmp_tables = LoadCsvIntoTempTablesTaskGroup(
                tables_to_insert=_tables_to_insert,
                task_group_id='create_and_load_tmp_tables_from_csv',
                sql_folder='etl',
            ).build()

            raw_tables_insert = TableOperationsTaskGroup(
                table_list=_table_manager.get_normalized_names(),
                sql_folder='etl',
                stage='raw',
                job_id=_job_id,
            ).build()

            typed_tables_insert = TableOperationsTaskGroup(
                table_list=_table_manager.get_normalized_names(),
                sql_folder='etl',
                stage='typed',
                job_id=_job_id,
            ).build()

            conform_tables_insert = TableOperationsTaskGroup(
                table_list=_conform_operations,
                sql_folder='etl',
                stage='conform',
                sequential=True,
                job_id=_job_id,
            ).build()

            staged_tables_insert = TableOperationsTaskGroup(
                table_list=_staged_operations,
                sql_folder='etl',
                stage='staged',
                sequential=True,
                job_id=_job_id,
            ).build()

            target_tables_insert = TableOperationsTaskGroup(
                table_list=_target_operations,
                sql_folder='etl',
                stage='target',
                sequential=True,
                job_id=_job_id,
            ).build()

            postprocessing_tables = TableOperationsTaskGroup(
                table_list=_postprocessing_operations,
                sql_folder='etl',
                stage='postprocessing',
                sequential=True,
                job_id=_job_id,
            ).build()

            report_broken_hierarchy = PythonOperator(
                task_id='report_broken_hierarchy',
                python_callable=send_broken_hierarchy_data,
                op_args=[_job_id],
            )

            clean_data = CleanDataTaskGroup(
                stage='cleanup',
                job_id=_job_id,
            ).build()

            notify_etl_start >> create_job_task >> load_missing_hierarchy_from_s3 >> \
                extract_from_pg >> \
                load_into_tmp_tables >> raw_tables_insert >> typed_tables_insert >>\
                conform_tables_insert >> staged_tables_insert >> target_tables_insert >> postprocessing_tables >>\
                report_broken_hierarchy >> clean_data

        return _dag
