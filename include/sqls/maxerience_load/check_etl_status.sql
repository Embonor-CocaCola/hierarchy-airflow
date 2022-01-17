select *
from airflow.dag_run dr
inner join airflow.etl_job ej  on dr.run_id = ej.dag_run_id
where ej.created_at::date = now()::date
and dr.dag_id = 'expos_etl'
and dr.run_type = 'scheduled'
and dr.state = 'success';
