import os

from airflow.utils.task_group import TaskGroup

from hierarchy_service.base.utils.tasks import arrange_task_list_sequentially
from hierarchy_service.config.common.settings import HIERARCHY_DATABASE_CONN_ID
from operators.postgres.query_with_params import PostgresOperatorWithParams


class TableOperationsTaskGroup:
    def __init__(
        self,
        table_list: list[str],
        stage: str,
        sql_folder,
        job_id=None,
        sequential=True,
        conn_id=HIERARCHY_DATABASE_CONN_ID,
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
        parameters = {'job_id': self.job_id}
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

    def build(self):
        tasks = list(map(lambda table_name: self.create_insert_task(
            table_name), self.tables_to_insert))
        if self.sequential:
            arrange_task_list_sequentially(tasks)

        return self.task_group
