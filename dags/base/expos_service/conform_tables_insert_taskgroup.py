import os

from airflow.utils.task_group import TaskGroup

from base.utils.tasks import arrange_task_list_sequentially
from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID
from operators.postgres.query_with_params import PostgresOperatorWithParams


class ConformTablesInsertTaskGroup:
    def __init__(self, tables_to_insert: list[str], task_group_id: str, job_id):
        if not tables_to_insert:
            raise ValueError('missing parameter tables_to_insert')

        self.tables_to_insert = tables_to_insert
        self.task_group = TaskGroup(group_id=task_group_id)
        self.job_id = job_id

    def create_insert_task(self, table_name: str):

        return PostgresOperatorWithParams(
            postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            task_id=f'insert_conform_{table_name}',
            task_group=self.task_group,
            sql=os.path.join(
                'expos_service', table_name, 'conform_data.sql',
            ),
            parameters={'job_id': self.job_id},
        )

    def build(self):
        arrange_task_list_sequentially(
            list(map(lambda table_name: self.create_insert_task(table_name), self.tables_to_insert)),
        )
        return self.task_group
