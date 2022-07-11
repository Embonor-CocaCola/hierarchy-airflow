DELETE FROM
    airflow.chief_plant_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.chief_plant_typed (
    chief_id,
    chief_code,
    chief_name,
    chief_location,
    chief_rut,
    plant_id,
    role,
    chief_unit,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(chief_id) :: INTEGER,
    trim(chief_code),
    trim(chief_name),
    trim(chief_location),
    trim(chief_rut),
    trim(plant_id) :: INTEGER,
    trim(role),
    trim(chief_unit),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.chief_plant_raw
WHERE job_id = %(job_id)s :: BIGINT
;
