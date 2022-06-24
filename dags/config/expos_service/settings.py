import os

airflow_root_dir = os.environ.get('AIRFLOW_HOME')

ES_EMBONOR_SERVICES_BASE_URL = os.environ.get('EMBONOR_SERVICES_BASE_URL')
ES_EMBONOR_SERVICES_BASE_URL_CONN_ID = 'embonor_services_base_conn'
ES_AIRFLOW_DATABASE_CONN_ID = 'airflow_db_conn'
ES_AIRFLOW_DATABASE_CONN_URI = os.environ.get('AIRFLOW__CORE__SQL_ALCHEMY_CONN')

ES_EXPOS_DATABASE_CONN_ID = 'expos_db_conn'
ES_EXPOS_DATABASE_CONN_URI = os.environ.get('EXPOS_DATABASE_CONN_URI')

ES_EMBONOR_PG_CONN_ID = 'embonor_pg_conn'
ES_EMBONOR_PG_CONN_URI = os.environ.get('EMBONOR_PG_CONN_URI')

ES_EMBONOR_MONGO_CONN_ID = 'mongo_default'  # this is mandatory because mongo hook always uses the default connection
ES_EMBONOR_MONGO_CONN_URI = os.environ.get('EMBONOR_MONGO_CONN_URI')
ES_EMBONOR_MONGO_DB_NAME = 'embonor-surveys'

ES_REMOTE_RDS_HOST = os.environ.get('EMBONOR_RDS_HOST')
ES_REMOTE_RDS_PORT = int(os.environ.get('EMBONOR_RDS_PORT', 5432))

ES_REMOTE_MONGO_HOST = os.environ.get('EMBONOR_MONGO_HOST')
ES_REMOTE_MONGO_PORT = int(os.environ.get('EMBONOR_MONGO_PORT', 27017))

ES_REMOTE_RDS_USER = os.environ.get('EMBONOR_RDS_USER')
ES_REMOTE_RDS_PASS = os.environ.get('EMBONOR_RDS_PASS')

ES_ETL_DAG_ID = 'expos_etl'
ES_ETL_DAG_START_DATE_VALUE = os.environ.get('ES_ETL_DAG_START_DATE_VALUE', '2021-11-24')
ES_ETL_DAG_SCHEDULE_INTERVAL = os.environ.get('ES_ETL_DAG_SCHEDULE_INTERVAL', '30 11 * * *')  # everyday at 11:30 UTC
ES_SQL_PATH = os.path.join(airflow_root_dir, 'include', 'sqls')
ES_ETL_CHECK_RUN_DAG_ID = 'expos_etl_check_run'

# every sunday at 23:59 UTC
ES_ETL_CHECK_RUN_DAG_SCHEDULE_INTERVAL = os.environ.get('ES_ETL_DAG_SCHEDULE_INTERVAL', '59 23 * * 0')

ES_SSH_CONN_ID = 'ssh_conn'
ES_SSH_CONN_URI = f'{os.environ.get("SSH_CONN_URI")}&private_key={os.environ.get("SSH_PRIVATE_KEY", "")}'

IS_LOCAL_RUN = os.environ.get('IS_LOCAL_RUN', False)
AUTH_USER = os.environ.get('AUTH_USER')
AUTH_PASS = os.environ.get('AUTH_PASS')

ES_PG_TABLES_TO_EXTRACT = os.environ.get(
    'ES_PG_TABLES_TO_EXTRACT',
    'Plants,BranchOffices,ChiefsPlants,SupervisorsPlants,Vendors,Customers,VendorsCustomers,VendorTypes,VendorsPlants',
).split(',')

ES_MONGO_COLLECTIONS_TO_EXTRACT = os.environ.get(
    'ES_MONGO_COLLECTIONS_TO_EXTRACT',
    'answers,questions,surveys',
).split(',')

ES_ETL_CONFORM_OPERATIONS_ORDER = os.environ.get(
    'ES_ETL_CONFORM_OPERATIONS_ORDER',
    'plant,branch_office,chief,supervisor,vendor_type,vendor_plant,vendor,cluster,customer,vendor_customer,question,survey,answer',  # noqa: E501
).split(',')

ES_ETL_STAGED_OPERATIONS_ORDER = os.environ.get(
    'ES_ETL_STAGED_OPERATIONS_ORDER',
    'plant,branch_office,chief,supervisor,vendor,cluster,customer,vendor_customer,question,survey,answer',
).split(',')

ES_ETL_TARGET_OPERATIONS_ORDER = os.environ.get(
    'ES_ETL_TARGET_OPERATIONS_ORDER',
    'plant,branch_office,chief,supervisor,vendor,cluster,customer,vendor_customer,question,survey,answer',
).split(',')

ES_ETL_POSTPROCESSING_OPERATIONS_ORDER = os.environ.get(
    'ES_ETL_TARGET_OPERATIONS_ORDER',
    'survey',
).split(',')

ES_STAGE = os.environ.get('STAGE', 'development')
ES_FETCH_OLD_EVALUATIONS_KEY = 'es_etl_fetch_old_self_evaluations'
