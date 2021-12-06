import os

from base.utils.table_names import TableNameManager
from airflow.utils.task_group import TaskGroup

from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID
from operators.postgres.query_with_params import PostgresOperatorWithParams


class TypedTablesInsertTaskGroup:
    def __init__(self, tables_to_insert: list[str], task_group_id: str, job_id):
        if not tables_to_insert:
            raise ValueError('missing parameter tables_to_insert')

        self.tables_to_insert = tables_to_insert
        self.task_group = TaskGroup(group_id=task_group_id)
        self.job_id = job_id

        self.table_name_manager = TableNameManager(tables_to_insert)

    def create_insert_task(self, original_table_name: str):
        table_names = self.table_name_manager.get_variations(original_table_name)

        return PostgresOperatorWithParams(
            postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
            task_id=f'insert_typed_{table_names["normalized"]}',
            task_group=self.task_group,
            sql=os.path.join(
                'expos_service', table_names['normalized'], 'typed_data.sql',
            ),
            parameters={'job_id': self.job_id},
        )

    def build(self):
        list(map(lambda table_name: self.create_insert_task(table_name), self.tables_to_insert))
        return self.task_group
