import os

from airflow.utils.task_group import TaskGroup

from base.utils.additional_sql_params import additional_params
from base.utils.tasks import arrange_task_list_sequentially
from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID, ES_STAGE
from operators.postgres.query_with_params import PostgresOperatorWithParams


class TablesInsertTaskGroup:
    def __init__(
        self,
        tables_to_insert: list[str],
        stage: str,
        job_id,
        sequential=True,
        conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
    ):

        if not tables_to_insert:
            raise ValueError('missing parameter tables_to_insert')

        self.conn_id = conn_id
        self.sequential = sequential
        self.stage = stage
        self.tables_to_insert = tables_to_insert
        self.task_group = TaskGroup(group_id=f'{stage}_tables_insert')
        self.job_id = job_id

    def create_insert_task(self, table_name: str):
        params_key = self.create_params_key(table_name)
        parameters = {'job_id': self.job_id} | additional_params.get(params_key, {})
        return PostgresOperatorWithParams(
            postgres_conn_id=self.conn_id,
            task_id=f'insert_{self.stage}_{table_name}',
            task_group=self.task_group,
            sql=os.path.join(
                'expos_service', table_name, f'{self.stage}_data.sql',
            ),
            parameters=parameters,
        )

    def create_params_key(self, table_name):
        return '.'.join([ES_STAGE, table_name, self.stage])

    def build(self):
        tasks = list(map(lambda table_name: self.create_insert_task(table_name), self.tables_to_insert))
        if self.sequential:
            arrange_task_list_sequentially(tasks)

        return self.task_group
