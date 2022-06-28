from airflow import DAG

from base.expos_service.etl_dag_factory import EtlDagFactory
from config.common.settings import STAGE

if STAGE == 'staging':
    dag: DAG = EtlDagFactory(check_run=True).build()
