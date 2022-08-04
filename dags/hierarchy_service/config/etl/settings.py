import os
import urllib.parse

HIERARCHY_EMBONOR_SERVICES_BASE_URL = os.environ.get('EMBONOR_SERVICES_BASE_URL')
HIERARCHY_EMBONOR_SERVICES_BASE_URL_CONN_ID = 'embonor_services_base_conn'

HIERARCHY_EMBONOR_PG_CONN_ID = 'embonor_pg_conn'
HIERARCHY_EMBONOR_PG_CONN_URI = os.environ.get('EMBONOR_PG_CONN_URI')

HIERARCHY_REMOTE_RDS_HOST = os.environ.get('EMBONOR_RDS_HOST')
HIERARCHY_REMOTE_RDS_PORT = int(os.environ.get('EMBONOR_RDS_PORT', 5432))

HIERARCHY_REMOTE_RDS_USER = os.environ.get('EMBONOR_RDS_USER')
HIERARCHY_REMOTE_RDS_PASS = os.environ.get('EMBONOR_RDS_PASS')

HIERARCHY_ETL_DAG_ID = 'hierarchy_etl'
HIERARCHY_ETL_DAG_START_DATE_VALUE = os.environ.get('HIERARCHY_ETL_DAG_START_DATE_VALUE', '2022-07-06')
# everyday at 09:30 UTC
HIERARCHY_ETL_DAG_SCHEDULE_INTERVAL = os.environ.get('HIERARCHY_ETL_DAG_SCHEDULE_INTERVAL', '30 09 * * *')

HIERARCHY_SSH_CONN_ID = 'ssh_conn'
HIERARCHY_SSH_PRIVATE_KEY = urllib.parse.quote_plus(os.environ.get('SSH_PRIVATE_KEY', '').replace(r'\n', '\n'))
HIERARCHY_SSH_CONN_URI = f'{os.environ.get("SSH_CONN_URI")}&private_key={HIERARCHY_SSH_PRIVATE_KEY}'

HIERARCHY_PG_TABLES_TO_EXTRACT = os.environ.get(
    'HIERARCHY_PG_TABLES_TO_EXTRACT',
    'Plants,BranchOffices,ChiefsPlants,SupervisorsPlants,Vendors,Customers,VendorsCustomers,VendorTypes,VendorsPlants',
).split(',')

HIERARCHY_ETL_CONFORM_OPERATIONS_ORDER = os.environ.get(
    'HIERARCHY_ETL_CONFORM_OPERATIONS_ORDER',
    'plant,branch_office,chief,supervisor,vendor_type,vendor_plant,vendor,cluster,customer,vendor_customer',  # noqa: E501
).split(',')

HIERARCHY_ETL_STAGED_OPERATIONS_ORDER = os.environ.get(
    'HIERARCHY_ETL_STAGED_OPERATIONS_ORDER',
    'plant,branch_office,chief,supervisor,vendor,cluster,customer,vendor_customer',
).split(',')

HIERARCHY_ETL_TARGET_OPERATIONS_ORDER = os.environ.get(
    'HIERARCHY_ETL_TARGET_OPERATIONS_ORDER',
    'plant,branch_office,chief,supervisor,vendor,cluster,customer,vendor_customer',
).split(',')

HIERARCHY_ETL_POSTPROCESSING_OPERATIONS_ORDER = os.environ.get(
    'HIERARCHY_ETL_TARGET_OPERATIONS_ORDER',
    '',
).split(',')
