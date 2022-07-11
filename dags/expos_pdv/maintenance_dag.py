from airflow import DAG
from expos_pdv.base.maintenance.maintenance_dag_factory import MaintenanceDagFactory

dag: DAG = MaintenanceDagFactory().build()
