from airflow import DAG

from base.expos_service.etl_dag_factory import EtlDagFactory
from config.expos_service.settings import ES_STAGE

if ES_STAGE == 'staging':
    dag: DAG = EtlDagFactory(check_run=True).build()
