from airflow import DAG

from base.run_sqls.run_sqls_dag_factory import RunSqlsDagFactory

dag: DAG = RunSqlsDagFactory.build()
