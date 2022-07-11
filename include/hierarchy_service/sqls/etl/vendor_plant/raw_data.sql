DELETE FROM
    airflow.vendor_plant_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_plant_raw (
    vendor_id,
    supervisor_id,
    vendor_name,
    chief_rut,
    plant_id,

    created_at,
    updated_at,
    job_id,
    id
)

SELECT
    vendorid,
    supervisorid,
    vendorName,
    chiefrut,
    plantid,

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()

FROM
    airflow.tmp_vendor_plant
;

DROP TABLE IF EXISTS airflow.tmp_vendor_plant;
