DELETE FROM
    airflow.plant_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.plant_conform (
    source_id,
    name,
    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    source_id,
    name,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.plant_typed
WHERE job_id = %(job_id)s :: BIGINT
;
