DELETE FROM
    airflow.vendor_plant_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_plant_typed (
    vendor_id,
    supervisor_id,
    chief_rut,
    plant_id,
    vendor_name,

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
    trim(vendor_name),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_plant_raw
WHERE job_id = %(job_id)s :: BIGINT
AND supervisor_id IS NOT NULL
;
