from airflow import DAG
from expos_pdv.base.maxerience_retrieve_result.maxerience_retrieve_result_dag_factory import \
    MaxerienceRetrieveResultDagFactory

dag: DAG = MaxerienceRetrieveResultDagFactory().build()
