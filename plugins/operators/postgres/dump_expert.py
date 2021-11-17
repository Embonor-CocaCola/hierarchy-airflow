from airflow.models import BaseOperator
from airflow.models.param import ParamsDict
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Dict


class PostgresOperatorDumpExpert(BaseOperator):

    template_fields = ('csv_path', 'parameters')
    template_ext = ('.sql',)

    def __init__(self, sql_path, postgres_conn_id, csv_path, parameters: Dict = None, include_headers=True, *args, **kwargs):
        super(PostgresOperatorDumpExpert, self).__init__(*args, **kwargs)

        self.sql_path = sql_path
        self.postgres_conn_id = postgres_conn_id
        self.csv_path = csv_path
        self.parameters = parameters
        self.params = ParamsDict(parameters)
        self.include_headers = include_headers

    def execute(self, context):
        with open(self.sql_path, 'r') as file:
            sql = file.read()

        if not sql:
            raise IOError('Missed query')

        if self.parameters:
            sql = sql % self.parameters

        sql = f"COPY ({sql}) TO STDOUT DELIMITER E',' CSV {'HEADER' if self.include_headers else ''}"

        self.log.debug(f'Dumping Postgres query results to local file {self.csv_path} using query "{sql}"')

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        hook.copy_expert(sql, self.csv_path)


class PostgresOperatorDumpExpertPlugin(AirflowPlugin):
    name = 'postgres_operator_dump_expert'
    operators = [PostgresOperatorDumpExpert]
