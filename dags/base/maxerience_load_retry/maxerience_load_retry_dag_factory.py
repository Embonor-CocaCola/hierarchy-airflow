import json
from datetime import datetime

from airflow.models import DAG
from airflow.operators.python import PythonOperator

from base.maxerience_load.utils.get_ir_api_key import get_ir_api_key
from base.maxerience_load_retry.utils.retry_uploads import retry_uploads
from base.utils.conditional_operator import conditional_operator
from base.utils.slack import notify_start_task
from config.common.defaults import default_dag_kwargs, default_task_kwargs
from config.expos_service.settings import ES_STAGE
from config.maxerience_load_retry.settings import (
    MLR_DAG_ID,
    MLR_DAG_SCHEDULE_INTERVAL,
    MLR_DAG_START_DATE_VALUE,
)


class MaxerienceLoadRetryDagFactory:
    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            MLR_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
        }

        with DAG(
                MLR_DAG_ID,
                **default_dag_kwargs,
                schedule_interval=MLR_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                user_defined_filters={
                    'fromjson': lambda s: json.loads(s), 'replace_single_quotes': lambda s: s.replace("'", '"'),
                },
        ) as _dag:

            notify_ml_dag_start = notify_start_task(_dag)

            get_api_key_task = conditional_operator(
                task_id='get_api_key',
                operator=PythonOperator,
                condition=ES_STAGE == 'production',
                python_callable=get_ir_api_key,
                dag=_dag,
            )

            retry_uploads_task = PythonOperator(
                task_id='retry_uploads',
                python_callable=retry_uploads,
                execution_timeout=None,
            )

            notify_ml_dag_start >> get_api_key_task >> retry_uploads_task

        return _dag
