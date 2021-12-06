DELETE FROM
    airflow.vendor_plant_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_plant_typed (
    vendor_id,
    supervisor_id,
    chief_rut,
    plant_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(vendor_id) :: INTEGER,
    trim(supervisor_id) :: INTEGER,
    trim(chief_rut),
    trim(plant_id) :: INTEGER,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_plant_raw
WHERE job_id = %(job_id)s :: BIGINT
;
