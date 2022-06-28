from airflow import DAG
from base.expos_service.etl_dag_factory import EtlDagFactory
from config.common.settings import STAGE

dag: DAG = EtlDagFactory(check_run=STAGE == 'development').build()
