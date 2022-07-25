DELETE FROM
    airflow.chief_plant_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.chief_plant_raw (
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
    chiefid,
    chiefcode,
    chiefname,
    chieflocation,
    chiefrut,
    plantid,
    role,
    chiefunit,
    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()

FROM
    airflow.tmp_chief_plant
;

DROP TABLE IF EXISTS airflow.tmp_chief_plant;
