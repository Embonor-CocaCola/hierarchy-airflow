from airflow import DAG
from base.expos_service.etl_dag_factory import EtlDagFactory
from config.expos_service.settings import ES_STAGE

dag: DAG = EtlDagFactory(check_run=ES_STAGE == 'development').build()
