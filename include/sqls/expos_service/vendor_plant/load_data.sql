DELETE FROM
    airflow.vendor_plant_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_plant_raw (
    vendor_id,
    supervisor_id,
    chief_rut,
    plant_id,

    created_at,
    updated_at,
    job_id
)

SELECT
    vendorid,
    supervisorid,
    chiefrut,
    plantid,

    now(),
    now(),
    %(job_id)s :: BIGINT
FROM
    airflow.tmp_vendor_plant
;

DROP TABLE IF EXISTS airflow.tmp_vendor_plant;
