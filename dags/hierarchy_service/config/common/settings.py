import os

from airflow.models import Variable

airflow_root_dir = os.environ.get('AIRFLOW_HOME')

STAGE = os.environ.get('STAGE', 'development')
IS_LOCAL_EXECUTION = os.environ.get('IS_LOCAL_RUN', False)
SHOULD_NOTIFY = STAGE in ['staging', 'production']  # and not IS_LOCAL_EXECUTION
SHOULD_USE_TUNNEL = STAGE in ['local'] or IS_LOCAL_EXECUTION

SLACK_WEBHOOK = Variable.get('pdv_slack_webhook')
SLACK_CHANNEL = Variable.get('pdv_slack_channel')
SLACK_EXPOS_BOT_TOKEN = Variable.get('pdv_bot_slack_token')

HIERARCHY_DATABASE_CONN_ID = 'hierarchy_db_conn_id'
SQL_PATH = os.path.join(airflow_root_dir, 'include', 'hierarchy_service', 'sqls')
EXPOS_S3_CONN_ID = 'expos_s3_conn'
