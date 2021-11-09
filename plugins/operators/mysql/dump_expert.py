import csv

from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.mysql.hooks.mysql import MySqlHook


class MySqlOperatorDumpExpert(BaseOperator):
    """
        Example:
            t = MySqlOperatorDumpExpert(
                task_id='t1_run',
                mysql_conn_id='default_conn_id',
                sql=os.path.join('dimensions', 'remote_data.sql'),
                csv_path='/tmp/temp.csv',
                parameters={'date': '2021-08-31'},
                dag=dag,
            )
        """
    chunk_size = 100
    template_fields = ('sql', 'parameters')
    template_ext = ('.sql',)
    ui_color = '#ededed'

    def __init__(self, sql, mysql_conn_id, csv_path, parameters=None, chunk_size=chunk_size, *args, **kwargs):
        super(MySqlOperatorDumpExpert, self).__init__(*args, **kwargs)

        self.sql = sql
        self.mysql_conn_id = mysql_conn_id
        self.csv_path = csv_path
        self.parameters = parameters
        self.params = parameters
        self.chunk_size = chunk_size

    def execute(self, context):
        self.log.debug(f'Dumping MySQL query results to local file {self.csv_path}')

        hook = MySqlHook(mysql_conn_id=self.mysql_conn_id)
        connection = hook.get_conn()
        cursor = connection.cursor()
        cursor.execute(query=self.sql)

        with open(self.csv_path, 'w', encoding='utf-8') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            header = []

            for field in cursor.description:
                header.append(field[0])

            csv_writer.writerow(header)
            rows = cursor.fetchmany(self.chunk_size)

            while len(rows) > 0:
                csv_writer.writerows(rows)
                rows = cursor.fetchmany(self.chunk_size)

            csv_file.flush()

        cursor.close()
        connection.close()


class MySqlOperatorDumpExpertPlugin(AirflowPlugin):
    name = 'mysql_operator_dump_expert'
    operators = [MySqlOperatorDumpExpert]
