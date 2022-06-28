from airflow import DAG
from base.expos_service.etl_dag_factory import EtlDagFactory

dag: DAG = EtlDagFactory().build()
