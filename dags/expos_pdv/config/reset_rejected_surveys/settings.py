import os

RRS_DAG_ID = 'reset_rejected_surveys_dag'
RRS_DAG_START_DATE_VALUE = os.environ.get('RRS_DAG_START_DATE', '2022-06-20')
RRS_DAG_SCHEDULE_INTERVAL = os.environ.get('RRS_DAG_SCHEDULE_INTERVAL', '0 2 * * *')  # Every day at 02:00 UTC
