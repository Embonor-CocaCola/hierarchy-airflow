from datetime import datetime

from airflow.models import DAG
from airflow.providers.postgres.operators.postgres import PostgresOperator

from base.utils.slack import notify_start_task
from config.common.defaults import default_dag_kwargs, default_task_kwargs
from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID
from config.maintenance.settings import MTNC_DAG_ID, MTNC_DAG_SCHEDULE_INTERVAL, MTNC_DAG_START_DATE_VALUE


class MaintenanceDagFactory:
    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            MTNC_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
        }

        with DAG(
                MTNC_DAG_ID,
                **default_dag_kwargs,
                schedule_interval=MTNC_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
        ) as _dag:

            notify_dag_start = notify_start_task(_dag)

            vacuum_analyze_db = PostgresOperator(
                dag=_dag,
                task_id='vacuum_analyze',
                sql='VACUUM ANALYZE',
                autocommit=True,
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            )

            notify_dag_start >> vacuum_analyze_db
        return _dag
