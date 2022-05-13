import os

from airflow.utils.task_group import TaskGroup

from base.utils.additional_sql_params import additional_params
from base.utils.tasks import arrange_task_list_sequentially
from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID, ES_STAGE
from operators.postgres.query_with_params import PostgresOperatorWithParams


class TableOperationsTaskGroup:
    def __init__(
        self,
        table_list: list[str],
        stage: str,
        sql_folder,
        job_id=None,
        sequential=True,
        conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
    ):

        if not table_list:
            raise ValueError('missing parameter table_list')

        self.conn_id = conn_id
        self.sequential = sequential
        self.stage = stage
        self.sql_folder = sql_folder
        self.tables_to_insert = table_list
        self.task_group = TaskGroup(group_id=f'{stage}_table_operations')
        self.job_id = job_id

    def create_insert_task(self, table_name: str):
        params_key = self.create_params_key(table_name)
        parameters = {'job_id': self.job_id} | additional_params.get(
            params_key, {})
        return PostgresOperatorWithParams(
            postgres_conn_id=self.conn_id,
            task_id=f'{self.stage}_{table_name}',
            task_group=self.task_group,
            sql=os.path.join(
                self.sql_folder, table_name, f'{self.stage}_data.sql',
            ),
            parameters=parameters,
            autocommit=True,
        )

    def create_params_key(self, table_name):
        return '.'.join([ES_STAGE, table_name, self.stage])

    def build(self):
        tasks = list(map(lambda table_name: self.create_insert_task(
            table_name), self.tables_to_insert))
        if self.sequential:
            arrange_task_list_sequentially(tasks)

        return self.task_group
