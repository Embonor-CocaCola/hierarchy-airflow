from datetime import datetime

from airflow.models import DAG

from base.expos_service.conform_tables_insert_taskgroup import ConformTablesInsertTaskGroup
from base.expos_service.extract_mongo_csv_taskgroup import \
    ExtractMongoCsvTaskGroup
from base.expos_service.extract_pg_csv_taskgroup import \
    ExtractPostgresCsvTaskGroup
from base.expos_service.health_checks_taskgroup import HealthChecksTaskGroup
from base.expos_service.raw_tables_insert_taskgroup import RawTablesInsertTaskGroup
from base.expos_service.typed_tables_insert_taskgroup import TypedTablesInsertTaskGroup
from base.utils.tunneler import Tunneler
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
    ES_ETL_CONFORM_OPERATIONS_ORDER,
)
from operators.postgres.create_job import PostgresOperatorCreateJob


class EtlDagFactory:
    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            ES_ETL_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'retries': 0,
            'retry_delay': 0,
        }
        _pg_table_list = ES_PG_TABLES_TO_EXTRACT
        _mongo_collection_list = ES_MONGO_COLLECTIONS_TO_EXTRACT
        _tables_to_insert = _pg_table_list + _mongo_collection_list
        _conform_operations = ES_ETL_CONFORM_OPERATIONS_ORDER

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
                catchup=False,
        ) as _dag:
            create_job_task = PostgresOperatorCreateJob(
                task_id='create_job',
                sql='insert_job.sql',
                dag=_dag,
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            )

            _job_id = PostgresOperatorCreateJob.get_job_id(_dag.dag_id, create_job_task.task_id)

            health_checks_task = HealthChecksTaskGroup(
                _dag, group_id='health_checks', pg_tunnel=pg_tunnel).build()

            extract_from_pg = ExtractPostgresCsvTaskGroup(
                _dag, group_id='extract_from_pg', pg_tunnel=pg_tunnel, table_list=_pg_table_list).build()

            extract_from_mongo = ExtractMongoCsvTaskGroup(
                _dag,
                group_id='extract_from_mongo',
                mongo_tunnel=mongo_tunnel,
                collection_list=_mongo_collection_list,
            ).build()

            raw_tables_insert = RawTablesInsertTaskGroup(
                tables_to_insert=_tables_to_insert,
                task_group_id='raw_tables_insert',
                job_id=_job_id,
            ).build()

            typed_tables_insert = TypedTablesInsertTaskGroup(
                tables_to_insert=_tables_to_insert,
                task_group_id='typed_tables_insert',
                job_id=_job_id,
            ).build()

            conform_tables_insert = ConformTablesInsertTaskGroup(
                tables_to_insert=_conform_operations,
                task_group_id='conform_tables_insert',
                job_id=_job_id,
            ).build()

            create_job_task >> health_checks_task >> [extract_from_pg, extract_from_mongo] >> raw_tables_insert
            raw_tables_insert >> typed_tables_insert >> conform_tables_insert

        return _dag
