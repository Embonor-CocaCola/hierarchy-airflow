from airflow import DAG
from expos_pdv.base.maxerience_load.maxerience_load_dag_factory import MaxerienceLoadDagFactory

dag: DAG = MaxerienceLoadDagFactory().build()
