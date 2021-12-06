import json

from airflow.models import BaseOperator
from airflow.models.param import ParamsDict
from airflow.plugins_manager import AirflowPlugin
from airflow.providers.postgres.hooks.postgres import PostgresHook
from typing import Dict


class PostgresOperatorWithParams(BaseOperator):
    """
    Example:
        t = PostgresOperatorWithParams(
            task_id='t1_run',
            postgres_conn_id='default_conn_id',
            sql=os.path.join('dimensions', 'raw_data.sql'),
            parameters={'file_path': tmp_file_path},
            dag=dag,
        )
    """
    template_fields = ('sql', 'parameters')
    template_ext = ('.sql',)
    ui_color = '#ededed'

    def __init__(
            self,
            sql: object,
            postgres_conn_id: object,
            parameters: Dict = None,
            autocommit: object = False,
            *args: object,
            **kwargs: object,
    ) -> object:
        super(PostgresOperatorWithParams, self).__init__(*args, **kwargs)

        self.sql = sql
        self.postgres_conn_id = postgres_conn_id
        self.autocommit = autocommit
        self.parameters = parameters
        self.params = ParamsDict(parameters)

    def execute(self, context):
        if isinstance(self.parameters, str):
            try:
                self.parameters = json.loads(self.parameters)
            except Exception:
                # so, it's not a json
                pass

        try:
            self.parameters.update(dict(context['dag_run'].conf['params']))
        except Exception:
            # so, don't exists context params
            pass

        hook = PostgresHook(postgres_conn_id=self.postgres_conn_id)
        hook.run(self.sql, self.autocommit, parameters=self.parameters)


class PostgresOperatorWithParamsPlugin(AirflowPlugin):
    name = 'postgres_operator_with_params'
    operators = [PostgresOperatorWithParams]
