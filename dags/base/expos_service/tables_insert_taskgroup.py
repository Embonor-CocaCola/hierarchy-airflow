import os

from airflow.utils.task_group import TaskGroup

from base.utils.tasks import arrange_task_list_sequentially
from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID
from operators.postgres.query_with_params import PostgresOperatorWithParams


class TablesInsertTaskGroup:
    def __init__(self, tables_to_insert: list[str], stage: str, job_id, sequential=False):
        if not tables_to_insert:
            raise ValueError('missing parameter tables_to_insert')

        self.sequential = sequential
        self.stage = stage
        self.tables_to_insert = tables_to_insert
        self.task_group = TaskGroup(group_id=f'{stage}_tables_insert')
        self.job_id = job_id

    def create_insert_task(self, table_name: str):

        return PostgresOperatorWithParams(
            postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            task_id=f'insert_{self.stage}_{table_name}',
            task_group=self.task_group,
            sql=os.path.join(
                'expos_service', table_name, f'{self.stage}_data.sql',
            ),
            parameters={'job_id': self.job_id},
        )

    def build(self):
        tasks = list(map(lambda table_name: self.create_insert_task(table_name), self.tables_to_insert))
        if self.sequential:
            arrange_task_list_sequentially(tasks)

        return self.task_group
