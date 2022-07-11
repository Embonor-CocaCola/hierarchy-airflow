DELETE FROM
    airflow.supervisor_plant_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.supervisor_plant_typed (
    supervisor_id,
    supervisor_code,
    supervisor_name,
    supervisor_location,
    chief_id,
    plant_id,
    role,
    chief_unit,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(supervisor_id) :: INTEGER,
    trim(supervisor_code),
    trim(supervisor_name),
    trim(supervisor_location),
    trim(chief_id) :: INTEGER,
    trim(plant_id) :: INTEGER,
    trim(role),
    trim(chief_unit),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.supervisor_plant_raw
WHERE job_id = %(job_id)s :: BIGINT
;
