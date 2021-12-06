import json
from contextlib import ExitStack

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.utils.task_group import TaskGroup
from base.utils.postgres import (
    PG_IS_ONLINE_QUERY,
    perform_pg_query,
    pg_online_check_result,
)
from config.expos_service.settings import (
    AUTH_PASS,
    AUTH_USER,
    ES_EMBONOR_PG_CONN_ID,
    ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
    IS_LOCAL_RUN,
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

    def set_token(self, ti):
        tokens = json.loads(
            ti.xcom_pull(task_ids=[f'{self.group_id}.get_auth_token'])[0])
        self.bearer_token = f'Bearer {tokens["token"]}'

    def check_pg_online_status(self) -> None:
        with self.pg_tunnel if IS_LOCAL_RUN else ExitStack():
            perform_pg_query(ES_EMBONOR_PG_CONN_ID, PG_IS_ONLINE_QUERY,
                             pg_online_check_result)

    def build(self) -> TaskGroup:
        task_group = TaskGroup(group_id=self.group_id)

        if IS_LOCAL_RUN:
            is_auth_service_available = HttpSensor(
                task_id='is_auth_service_available',
                task_group=task_group,
                http_conn_id=ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
                endpoint='auth-service/api/health',
                response_check=lambda response: response.status_code == 200,
                poke_interval=5,
                timeout=15,
            )
            get_auth_token = SimpleHttpOperator(
                task_id='get_auth_token',
                task_group=task_group,
                http_conn_id=ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
                endpoint='auth-service/api/login',
                method='POST',
                data=json.dumps({
                    'username': AUTH_USER,
                    'password': AUTH_PASS,
                    'refreshToken': True,
                    'context': 'cl',
                }),
                headers={'Content-Type': 'application/json'},
                do_xcom_push=True,
            )
            retrieve_and_store_tokens = PythonOperator(
                task_id='retrieve_and_store_tokens',
                task_group=task_group,
                python_callable=self.set_token,
            )

        is_base_service_database_online = PythonOperator(
            task_id='is_base_service_database_online',
            task_group=task_group,
            python_callable=self.check_pg_online_status,
        )

        if IS_LOCAL_RUN:
            is_auth_service_available >> get_auth_token >> retrieve_and_store_tokens >> is_base_service_database_online

        return task_group
