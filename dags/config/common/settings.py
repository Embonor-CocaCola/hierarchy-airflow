import os

from config.expos_service.settings import ES_STAGE, IS_LOCAL_RUN

airflow_root_dir = os.environ.get('AIRFLOW_HOME')

SLACK_SUCCESS_CHANNEL_URL = os.environ.get('SLACK_SUCCESS_CHANNEL_URL')
SLACK_FAILURE_CHANNEL_URL = os.environ.get('SLACK_FAILURE_CHANNEL_URL')
ES_AIRFLOW_DATABASE_CONN_URI = os.environ.get('AIRFLOW__CORE__SQL_ALCHEMY_CONN')
SHOULD_NOTIFY = ES_STAGE in ['staging', 'production'] and not IS_LOCAL_RUN
EXPOS_DATABASE_CONN_ID = 'expos_db_conn_id'
