from airflow import DAG
from base.reset_rejected_surveys.reset_rejected_surveys_dag_factory import ResetRejectedSurveysDagFactory

dag: DAG = ResetRejectedSurveysDagFactory.build()
