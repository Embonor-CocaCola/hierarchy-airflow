DELETE FROM
    airflow.supervisor_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.supervisor_conform (
    source_id,
    name,
    plant_id,
    code,
    location,
    role,
    chief_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    supervisor_id,
    INITCAP(supervisor_name),
    plant_id,
    supervisor_code,
    supervisor_location,
    role,
    chief_id,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.supervisor_plant_typed
WHERE job_id = %(job_id)s :: BIGINT
;
