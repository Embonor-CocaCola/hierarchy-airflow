import os

from config.expos_service.settings import airflow_root_dir

MRR_DAG_ID = 'maxerience_retrieve_result'
MRR_DAG_START_DATE_VALUE = os.environ.get('MRR_DAG_START_DATE', '2022-02-23')
MRR_DAG_SCHEDULE_INTERVAL = os.environ.get('MRR_DAG_SCHEDULE_INTERVAL', '0 15 * * *')  # everyday at 15:00 UTC
MRR_SQL_PATH = os.path.join(airflow_root_dir, 'include', 'sql')
MRR_SAS_KEY = os.environ.get('MRR_SAS_KEY')
MRR_REST_BASE_URL = os.environ.get('MRR_MAXERIENCE_REST_BASE_URL')
