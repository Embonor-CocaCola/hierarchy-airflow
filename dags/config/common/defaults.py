from datetime import timedelta

from base.utils.slack import on_success_callback, on_failure_callback
from config.expos_service.settings import ES_SQL_PATH

default_dag_kwargs = {
    'template_searchpath': ES_SQL_PATH,
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
