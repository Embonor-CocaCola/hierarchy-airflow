DELETE FROM
    airflow.chief_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.chief_conform (
    source_id,
    name,
    plant_id,
    code,
    location,
    rut,
    role,
    unit,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    chief_id,
    chief_name,
    plant_id,
    chief_code,
    chief_location,
    chief_rut,
    role,
    chief_unit,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.chief_plant_typed
WHERE job_id = %(job_id)s :: BIGINT
;
