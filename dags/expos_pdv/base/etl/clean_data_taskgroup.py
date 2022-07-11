import os

from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.utils.task_group import TaskGroup

from expos_pdv.base.utils.tasks import arrange_task_list_sequentially
from expos_pdv.config.common.settings import SQL_PATH
from expos_pdv.config.etl.settings import ES_AIRFLOW_DATABASE_CONN_ID
from psycopg2 import sql


class CleanDataTaskGroup:
    def __init__(
        self,
        stage: str,
        job_id,
        max_antiquity_allowed='1 month',
        conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
    ):
        self.max_antiquity_allowed = max_antiquity_allowed
        self.conn_id = conn_id
        self.stage = stage
        self.task_group = TaskGroup(group_id=f'{stage}_tables')
        self.job_id = job_id
        self.base_dir = f'{SQL_PATH}/etl'
        self.steps_for_cleanup = ['raw', 'typed', 'conform', 'staged']

    def execute_sql_with_table_as_parameter(self, table_name, max_age):
        hook = PostgresHook(postgres_conn_id=self.conn_id)
        with hook.get_conn() as conn:
            with conn.cursor() as cursor:
                cursor.execute(sql.SQL('DELETE FROM {} WHERE created_at < now() - INTERVAL %(max_age)s;').format(
                    sql.Identifier(table_name),
                ), {'max_age': max_age})

                print(f'Rows affected = {cursor.rowcount}')

    def create_cleanup_task(self, table_name: str, task_group):
        parameters = {
            'max_age': self.max_antiquity_allowed,
            'table_name': table_name,
        }

        PythonOperator(
            task_id=f'{self.stage}_{table_name}',
            task_group=task_group,
            op_kwargs=parameters,
            python_callable=self.execute_sql_with_table_as_parameter,
        )

    def create_cleanup_group(self, dir_name):
        task_group = TaskGroup(group_id=f'{self.stage}_{dir_name}')
        folder_files = list(os.listdir(f'{self.base_dir}/{dir_name}'))
        sql_files = filter(
            lambda filename: filename.split('_')[0] in self.steps_for_cleanup,
            folder_files,
        )
        list(
            map(
                lambda filename: self.create_cleanup_task(f'{dir_name}_{filename.split("_")[0]}', task_group),
                sql_files,
            ),
        )
        return task_group

    def build(self):
        with self.task_group as tg:

            table_dirs = filter(
                lambda filename: os.path.isdir(f'{self.base_dir}/{filename}'),
                list(os.listdir(self.base_dir)),
            )

            tasks = list(map(lambda dir_name: self.create_cleanup_group(dir_name), table_dirs))

            arrange_task_list_sequentially(tasks)

            return tg
