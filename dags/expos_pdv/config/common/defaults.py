from datetime import timedelta

from expos_pdv.base.utils.slack import on_success_callback, on_failure_callback
from expos_pdv.config.common.settings import SQL_PATH

default_dag_kwargs = {
    'template_searchpath': SQL_PATH,
    'max_active_runs': 1,
    'on_success_callback': on_success_callback,
    'catchup': False,
}

default_task_kwargs = {
    'owner': 'airflow',
    'provide_context': True,
    'execution_timeout': timedelta(minutes=10),
    'retries': 0,
    'on_failure_callback': on_failure_callback,
}
