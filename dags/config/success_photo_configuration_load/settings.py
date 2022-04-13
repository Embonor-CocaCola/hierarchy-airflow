import os

SPCL_DAG_START_DATE_VALUE = os.environ.get(
    'SPCL_DAG_START_DATE_VALUE', '2022-03-25')
SPCL_DAG_ID = 'success_photo_configuration_load'
SPCL_DAG_SCHEDULE_INTERVAL = os.environ.get(
    'SPCL_DAG_SCHEDULE_INTERVAL', '0 11 * * 1')
SPCL_TABLES_TO_EXTRACT = os.environ.get(
    'SPCL_TABLES_TO_EXTRACT',
    'Dictionary,SuccessPhotoProduct',
).split(',')
SPCL_S3_CONN_ID = 'SPCL_S3_CONN'
