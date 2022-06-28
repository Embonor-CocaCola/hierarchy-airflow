import os

from config.expos_service.settings import IS_LOCAL_RUN

airflow_root_dir = os.environ.get('AIRFLOW_HOME')
STAGE = os.environ.get('STAGE', 'development')

SHOULD_NOTIFY = STAGE in ['staging', 'production'] and not IS_LOCAL_RUN
SHOULD_USE_TUNNEL = STAGE in ['local', 'development'] or IS_LOCAL_RUN

SLACK_SUCCESS_CHANNEL_URL = os.environ.get('SLACK_SUCCESS_CHANNEL_URL')
SLACK_FAILURE_CHANNEL_URL = os.environ.get('SLACK_FAILURE_CHANNEL_URL')

ES_AIRFLOW_DATABASE_CONN_URI = os.environ.get('AIRFLOW__CORE__SQL_ALCHEMY_CONN')
EXPOS_DATABASE_CONN_ID = 'expos_db_conn_id'
SLACK_EXPOS_BOT_TOKEN = os.environ.get('SLACK_EXPOS_BOT_TOKEN')
SLACK_ETL_SUCCESS_CHANNEL = os.environ.get('SLACK_ETL_SUCCESS_CHANNEL')
SHOULD_UPLOAD_TO_S3 = STAGE == 'production' and not IS_LOCAL_RUN
SURVEY_SERVICE_BASE_URL = os.environ.get('SURVEYS_SERVICE_BASE_URL')
