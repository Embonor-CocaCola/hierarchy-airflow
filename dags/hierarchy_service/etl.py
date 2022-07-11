from airflow import DAG
from hierarchy_service.base.etl.etl_dag_factory import EtlDagFactory

dag: DAG = EtlDagFactory().build()
