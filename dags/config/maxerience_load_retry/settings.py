import os

from config.common.settings import airflow_root_dir

MLR_DAG_ID = 'maxerience_load_retry'
MLR_DAG_START_DATE_VALUE = os.environ.get('MLR_DAG_START_DATE', '2022-03-03')
MLR_DAG_SCHEDULE_INTERVAL = os.environ.get('MLR_DAG_SCHEDULE_INTERVAL', '0 21 * * *')  # everyday at 21:00 UTC
MLR_SQL_PATH = os.path.join(airflow_root_dir, 'include', 'sql')
