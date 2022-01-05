import json

from airflow.models.dag import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.utils.task_group import TaskGroup

from config.expos_service.settings import (
    AUTH_PASS,
    AUTH_USER,
    ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
)


class SmplHealthChecksTaskGroup:
    def __init__(self, dag: DAG, group_id: str) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.dag = dag
        self.group_id = group_id
        self.retrieve_and_store_tokens = None

    def build(self) -> TaskGroup:
        task_group = TaskGroup(group_id=self.group_id)

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

        is_auth_service_available >> get_auth_token

        return task_group
