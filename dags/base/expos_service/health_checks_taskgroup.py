from contextlib import ExitStack

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator

from airflow.utils.task_group import TaskGroup
from base.utils.postgres import (
    PG_IS_ONLINE_QUERY,
    perform_pg_query,
    pg_online_check_result,
)
from config.common.settings import SHOULD_USE_TUNNEL
from config.expos_service.settings import (
    ES_EMBONOR_PG_CONN_ID,
)


class HealthChecksTaskGroup:
    bearer_token: str

    def __init__(self, dag: DAG, group_id: str, pg_tunnel) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.dag = dag
        self.group_id = group_id
        self.pg_tunnel = pg_tunnel

    def check_pg_online_status(self) -> None:
        with self.pg_tunnel if SHOULD_USE_TUNNEL else ExitStack():
            perform_pg_query(ES_EMBONOR_PG_CONN_ID, PG_IS_ONLINE_QUERY,
                             pg_online_check_result)

    def build(self) -> TaskGroup:
        task_group = TaskGroup(group_id=self.group_id)

        PythonOperator(
            task_id='is_base_service_database_online',
            task_group=task_group,
            python_callable=self.check_pg_online_status,
        )

        return task_group
