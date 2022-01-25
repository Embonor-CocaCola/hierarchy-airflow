from datetime import datetime, timedelta

from airflow.models import DAG
from airflow.operators.python import PythonOperator

from base.expos_service.clean_data_taskgroup import CleanDataTaskGroup
from base.expos_service.load_csv_into_temp_tables_taskgroup import LoadCsvIntoTempTablesTaskGroup
from base.expos_service.tables_insert_taskgroup import TablesInsertTaskGroup
from base.expos_service.extract_docdb_csv_taskgroup import \
    ExtractDocumentDbCsvTaskGroup
from base.expos_service.extract_pg_csv_taskgroup import \
    ExtractPostgresCsvTaskGroup
from base.expos_service.health_checks_taskgroup import HealthChecksTaskGroup
from base.utils.slack import build_etl_status_msg, send_slack_notification
from base.utils.table_names import TableNameManager
from base.utils.tunneler import Tunneler
from config.common.settings import SHOULD_NOTIFY
from config.expos_service.settings import (
    ES_AIRFLOW_DATABASE_CONN_ID,
    ES_ETL_DAG_ID,
    ES_ETL_DAG_SCHEDULE_INTERVAL,
    ES_ETL_DAG_START_DATE_VALUE,
    ES_REMOTE_MONGO_HOST,
    ES_REMOTE_MONGO_PORT,
    ES_REMOTE_RDS_HOST,
    ES_REMOTE_RDS_PORT, ES_SQL_PATH,
    IS_LOCAL_RUN,
    ES_MONGO_COLLECTIONS_TO_EXTRACT,
    ES_PG_TABLES_TO_EXTRACT,
    ES_ETL_CONFORM_OPERATIONS_ORDER, ES_ETL_STAGED_OPERATIONS_ORDER, ES_ETL_TARGET_OPERATIONS_ORDER,
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
                                payload=build_etl_status_msg(status='failed',
                                                             mappings={'run_id': run_id, 'task_id': ti.task_id}))

    @staticmethod
    def on_success_callback(context):
        if not SHOULD_NOTIFY:
            return

        run_id = context['run_id']
        send_slack_notification(notification_type='success',
                                payload=build_etl_status_msg(status='finished',
                                                             mappings={'run_id': run_id}))

    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            ES_ETL_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(seconds=180),
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
                    op_kwargs={'payload': build_etl_status_msg(status='started', mappings={'run_id': '{{ run_id }}'}),
                               'notification_type': 'success'},
                    python_callable=send_slack_notification,
                    dag=_dag,
                )

            health_checks_task = HealthChecksTaskGroup(
                _dag, group_id='health_checks', pg_tunnel=pg_tunnel).build()

            extract_from_pg = ExtractPostgresCsvTaskGroup(
                _dag, group_id='extract_from_pg', pg_tunnel=pg_tunnel, table_list=_pg_table_list).build()

            extract_from_mongo = ExtractDocumentDbCsvTaskGroup(
                _dag,
                group_id='extract_from_document_db',
                mongo_tunnel=mongo_tunnel,
                collection_list=_mongo_collection_list,
            ).build()

            load_into_tmp_tables = LoadCsvIntoTempTablesTaskGroup(
                tables_to_insert=_tables_to_insert,
                task_group_id='create_and_load_tmp_tables_from_csv',
            ).build()

            raw_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_table_manager.get_normalized_names(),
                stage='raw',
                job_id=_job_id,
            ).build()

            typed_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_table_manager.get_normalized_names(),
                stage='typed',
                job_id=_job_id,
            ).build()

            conform_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_conform_operations,
                stage='conform',
                sequential=True,
                job_id=_job_id,
            ).build()

            staged_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_staged_operations,
                stage='staged',
                sequential=True,
                job_id=_job_id,
            ).build()

            target_tables_insert = TablesInsertTaskGroup(
                tables_to_insert=_target_operations,
                stage='target',
                sequential=True,
                job_id=_job_id,
            ).build()

            clean_data = CleanDataTaskGroup(
                stage='cleanup',
                job_id=_job_id,
            ).build()

            if SHOULD_NOTIFY:
                create_job_task >> notify_etl_start >> health_checks_task
            else:
                create_job_task >> health_checks_task

            health_checks_task >> [extract_from_pg, extract_from_mongo] >> load_into_tmp_tables
            load_into_tmp_tables >> raw_tables_insert >> typed_tables_insert >> conform_tables_insert
            conform_tables_insert >> staged_tables_insert >> target_tables_insert >> clean_data

        return _dag
