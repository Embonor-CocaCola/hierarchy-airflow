from contextlib import ExitStack
from logging import info

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.task_group import TaskGroup

from base.utils.tasks import arrange_task_list_sequentially
from base.utils.tunneler import Tunneler
from config.common.settings import SHOULD_USE_TUNNEL
from config.expos_service.settings import (
    ES_EMBONOR_PG_CONN_ID,
)


class ExtractPostgresCsvTaskGroup:
    def __init__(self, dag: DAG, group_id: str, pg_tunnel: Tunneler, table_list: list) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')
        if SHOULD_USE_TUNNEL and not pg_tunnel:
            raise ValueError('pg_tunnel must be supplied for local runs')

        self.dag = dag
        self.group_id = group_id
        self.table_list = table_list
        self.pg_tunnel = pg_tunnel

    def extract_csv(self, table_name):
        with self.pg_tunnel if SHOULD_USE_TUNNEL else ExitStack():
            info(f'Starting extraction from postgres table: {table_name}...')

            pg_hook = PostgresHook(postgres_conn_id=ES_EMBONOR_PG_CONN_ID,
                                   schema='embonor')
            conn = pg_hook.get_conn()
            print('pg conn acquired')
            with conn.cursor() as cursor:
                print('pg cursor acquired')

                with open(f'/opt/airflow/data/{table_name}.csv', 'w') as file:
                    print('file opened')

                    cursor.copy_expert(
                        f'COPY "{table_name}" TO STDOUT WITH CSV HEADER', file)
            conn.commit()
            conn.close()
        print('extract finished')

    def create_extract_task(self, table, task_group):
        return PythonOperator(
            task_id=f'extract_{table}_to_csv',
            task_group=task_group,
            python_callable=self.extract_csv,
            op_args=[table],
        )

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        extract_tasks = list(
            map(
                lambda table: self.create_extract_task(table, task_group),
                self.table_list,
            ))

        arrange_task_list_sequentially(extract_tasks)

        return task_group
