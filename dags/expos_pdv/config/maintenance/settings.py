import os

MTNC_DAG_ID = 'maintenance_dag'
MTNC_DAG_START_DATE_VALUE = os.environ.get('MTNC_DAG_START_DATE', '2022-05-31')
MTNC_DAG_SCHEDULE_INTERVAL = os.environ.get('MTNC_DAG_SCHEDULE_INTERVAL', '0 7 * * *')  # everyday at 7:00 UTC
