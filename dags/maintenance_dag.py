from airflow import DAG
from base.maintenance.maintenance_dag_factory import MaintenanceDagFactory

dag: DAG = MaintenanceDagFactory().build()
