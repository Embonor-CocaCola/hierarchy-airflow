import os

airflow_root_dir = os.environ.get('AIRFLOW_HOME')
AIRFLOW_DATABASE_CONN_URI = os.environ.get('AIRFLOW__CORE__SQL_ALCHEMY_CONN')

STAGE = os.environ.get('STAGE', 'development')
IS_LOCAL_EXECUTION = os.environ.get('IS_LOCAL_RUN', False)
SHOULD_NOTIFY = STAGE in ['staging', 'production']  # and not IS_LOCAL_EXECUTION
SHOULD_USE_TUNNEL = STAGE in ['local'] or IS_LOCAL_EXECUTION

SLACK_CHANNEL_URL = os.environ.get('HIERARCHY_SLACK_CHANNEL_URL')
SLACK_EXPOS_BOT_TOKEN = os.environ.get('SLACK_EXPOS_BOT_TOKEN')

HIERARCHY_DATABASE_CONN_ID = 'hierarchy_db_conn_id'
SQL_PATH = os.path.join(airflow_root_dir, 'include', 'hierarchy_service', 'sqls')
