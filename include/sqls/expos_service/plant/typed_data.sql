DELETE FROM
    airflow.plant_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.plant_typed (
    source_id,
    name,
    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(source_id) :: INTEGER,
    trim(name),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.plant_raw
WHERE job_id = %(job_id)s :: BIGINT
;
