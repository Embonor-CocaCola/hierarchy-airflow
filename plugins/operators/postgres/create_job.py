from airflow.models import BaseOperator
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.postgres.hooks.postgres import PostgresHook


class PostgresOperatorCreateJob(BaseOperator):
    JOB_ID_KEY = 'job_id'

    template_fields = ('sql',)
    template_ext = ('.sql',)
    ui_color = '#ededed'

    def __init__(self, sql, postgres_conn_id, *args, **kwargs):
        super(PostgresOperatorCreateJob, self).__init__(*args, **kwargs)

        self.sql = sql
        self.postgres_conn_id = postgres_conn_id

    def execute(self, context):
        self.log.debug(f'Creating job using: {self.sql}')

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        engine = hook.get_sqlalchemy_engine()
        cursor = engine.execute(self.sql, dag_run_id=context['dag_run'].run_id)
        job = cursor.fetchone()

        context['task_instance'].xcom_push(
            key=self.JOB_ID_KEY,
            value=job[0],
        )

    @classmethod
    def get_job_id(cls, dag_id, task_id):
        return "{{ task_instance.xcom_pull(dag_id='%s', task_ids='%s', key='%s') }}" % (
            dag_id,
            task_id,
            cls.JOB_ID_KEY,
        )

    @classmethod
    def get_execution_date(cls):
        return "{{ execution_date.strftime('%Y-%m-%d') }}"


class PostgresOperatorCreateJobPlugin(AirflowPlugin):
    name = 'postgres_operator_create_job'
    operators = [PostgresOperatorCreateJob]
