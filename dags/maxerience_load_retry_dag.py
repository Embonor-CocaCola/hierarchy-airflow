from airflow import DAG
from base.maxerience_load_retry.maxerience_load_retry_dag_factory import MaxerienceLoadRetryDagFactory

dag: DAG = MaxerienceLoadRetryDagFactory.build()
