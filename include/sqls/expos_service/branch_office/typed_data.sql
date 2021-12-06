DELETE FROM
    airflow.branch_office_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.branch_office_typed (
    source_id,
    name,
    plant_id,
    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(source_id) :: INTEGER,
    trim(name),
    trim(plant_id) :: INTEGER,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.branch_office_raw
WHERE job_id = %(job_id)s :: BIGINT
;
