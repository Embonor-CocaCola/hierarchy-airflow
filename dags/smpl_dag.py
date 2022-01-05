from airflow import DAG
from base.survey_monthly_photo_loader.smpl_dag_factory import SmplDagFactory

dag: DAG = SmplDagFactory().build()
