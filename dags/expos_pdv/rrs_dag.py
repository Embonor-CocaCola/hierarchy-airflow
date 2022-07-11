from airflow import DAG
from expos_pdv.base.reset_rejected_surveys.reset_rejected_surveys_dag_factory import ResetRejectedSurveysDagFactory

dag: DAG = ResetRejectedSurveysDagFactory.build()
