from airflow import DAG
from expos_pdv.base.etl.etl_dag_factory import EtlDagFactory
from expos_pdv.config.common.settings import STAGE

if STAGE == 'staging':
    dag: DAG = EtlDagFactory(check_run=True).build()
