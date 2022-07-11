INSERT INTO airflow.etl_job
(
    dag_run_id,
    attempt,
    created_at
)
SELECT
    %(dag_run_id)s :: VARCHAR,
    COALESCE(max(attempt) + 1, 0),
    now()
FROM
    airflow.etl_job
WHERE
    dag_run_id = %(dag_run_id)s :: VARCHAR
RETURNING id;
