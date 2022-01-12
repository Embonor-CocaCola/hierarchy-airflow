select * from airflow.dag_run where execution_date::date = now()::date and dag_id = 'expos_etl' and run_type = 'scheduled' and state = 'success';
