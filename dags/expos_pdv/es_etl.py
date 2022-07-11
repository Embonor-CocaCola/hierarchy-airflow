from airflow import DAG
from expos_pdv.base.etl.etl_dag_factory import EtlDagFactory

dag: DAG = EtlDagFactory().build()
