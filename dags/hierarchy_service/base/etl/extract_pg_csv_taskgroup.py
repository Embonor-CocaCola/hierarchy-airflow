from contextlib import ExitStack
from logging import info

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.task_group import TaskGroup

from hierarchy_service.base.utils.tasks import arrange_task_list_sequentially
from hierarchy_service.base.utils.tunneler import Tunneler
from hierarchy_service.config.common.settings import SHOULD_USE_TUNNEL
from hierarchy_service.config.etl.settings import (
    HIERARCHY_EMBONOR_PG_CONN_ID,
)


class ExtractPostgresCsvTaskGroup:
    def __init__(self, dag: DAG, group_id: str, pg_tunnel: Tunneler, table_list: list,
                 conn_id=HIERARCHY_EMBONOR_PG_CONN_ID, db_name='embonor') -> None:
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
        self.conn_id = conn_id
        self.db_name = db_name

    def extract_csv(self, table_name):
        with self.pg_tunnel if SHOULD_USE_TUNNEL else ExitStack():
            info(f'Starting extraction from postgres table: {table_name}...')

            pg_hook = PostgresHook(postgres_conn_id=self.conn_id,
                                   schema=self.db_name)
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
