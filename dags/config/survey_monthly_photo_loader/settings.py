import os

SMPL_DAG_ID = 'survey_monthly_photo_loader'
SMPL_DAG_START_DATE_VALUE = os.environ.get('SMPL_DAG_START_DATE_VALUE', '2022-01-01')
SMPL_SELF_EVALUATION_SURVEY_ID = os.environ.get('SMPL_SELF_EVALUATION_SURVEY_ID', '6183e40c889a0f0013010903')
PRE_AUTHENTICATED_REQUESTS_URL = os.environ.get('PRE_AUTHENTICATED_REQUESTS_URL')
OCI_USER = os.environ.get('OCI_USER')
OCI_KEY = os.environ.get('OCI_KEY')
OCI_FINGERPRINT = os.environ.get('OCI_FINGERPRINT')
OCI_TENANCY = os.environ.get('OCI_TENANCY')
OCI_REGION = os.environ.get('OCI_REGION')
