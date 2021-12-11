import os
from contextlib import closing

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresOperatorCopyExpert(BaseOperator):
    template_fields = 'csv_path', 'additional_values'

    def __init__(self, postgres_conn_id, table, csv_path, column_names=None, additional_columns=None,
                 additional_values=None, *args, **kwargs):
        super(PostgresOperatorCopyExpert, self).__init__(*args, **kwargs)

        self.postgres_conn_id = postgres_conn_id
        self.table = table
        self.csv_path = csv_path
        self.column_names = column_names
        self.additional_columns = additional_columns
        self.additional_values = additional_values

    def execute(self, context):
        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        if self.additional_columns:
            self.copy_with_temporary_table(hook)
        else:
            self.copy(hook)

    @staticmethod
    def enclose(sql):
        if sql:
            return f'( {sql} )'
        return sql

    def copy(self, hook):
        self.log.debug(f'Copying data to table {self.table}')

        if not os.path.isfile(self.csv_path):
            raise FileNotFoundError(f'CSV file {self.csv_path} not found')
        hook.copy_expert(
            f"COPY {self.table}{self.enclose(self.columns)} FROM STDIN DELIMITER E',' CSV HEADER",
            self.csv_path,
        )

    def copy_with_temporary_table(self, hook):
        temporary_table_name = 'temporary_copy_expert_table'
        with open(self.csv_path, 'r+') as f:
            with closing(hook.get_conn()) as conn:
                with closing(conn.cursor()) as cursor:
                    cursor.execute(f'CREATE TEMP TABLE {temporary_table_name}({self.temp_columns_schema});')
                    cursor.copy_expert(f"COPY {temporary_table_name} FROM STDIN DELIMITER E',' CSV HEADER;", f)
                    cursor.execute(f"""
                        INSERT INTO {self.table}{self.enclose(self.columns + ',' + self.additional_columns)}
                        SELECT {self.columns}, {self.additional_values}
                        FROM {temporary_table_name};
                    """)
                    f.truncate(f.tell())
                    conn.commit()

    @property
    def columns(self):
        if self.column_names:
            return f'{",".join(self.column_names)}'
        return ''

    @property
    def temp_columns_schema(self):
        return ','.join([f'{column} TEXT' for column in self.column_names])


class PostgresOperatorCopyExpertPlugin(AirflowPlugin):
    name = 'postgres_operator_copy_expert'
    operators = [PostgresOperatorCopyExpert]
