DELETE FROM
    airflow.chief_conform
WHERE
    job_id = %(job_id)s :: BIGINT;
ANALYZE airflow.chief_conform;

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
    INITCAP(chief_name),
    plant_id,
    chief_code,
    INITCAP(chief_location),
    chief_rut,
    INITCAP(role),
    chief_unit,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.chief_plant_typed
WHERE job_id = %(job_id)s :: BIGINT
;
ANALYZE airflow.chief_conform;
