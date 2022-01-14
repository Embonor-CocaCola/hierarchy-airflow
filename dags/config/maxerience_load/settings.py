import os

from config.expos_service.settings import airflow_root_dir

ML_DAG_ID = 'maxerience_load'
ML_DAG_START_DATE_VALUE = os.environ.get('ML_DAT_START_DATE', '2022-01-01')
ML_DAG_SCHEDULE_INTERVAL = os.environ.get('ML_DAG_SCHEDULE_INTERVAL', '0 12 * * *')  # everyday at 12:00 UTC
ML_SQL_PATH = os.path.join(airflow_root_dir, 'include', 'sqls')
ML_AIRFLOW_DATABASE_CONN_ID = 'ml_airflow_db_conn_id'
ML_MAXERIENCE_BASE_URL = os.environ.get('ML_MAXERIENCE_BASE_URL')
ML_MAXERIENCE_USER = os.environ.get('ML_MAXERIENCE_USER')
ML_MAXERIENCE_PASS = os.environ.get('ML_MAXERIENCE_PASS')
