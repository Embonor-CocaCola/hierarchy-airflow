DELETE FROM
    airflow.supervisor_plant_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.supervisor_plant_raw (
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
    job_id
)
SELECT
    supervisorid,
    supervisorcode,
    supervisorname,
    supervisorlocation,
    chiefid,
    plantid,
    role,
    chiefunit,

    now(),
    now(),
    %(job_id)s :: BIGINT
FROM
    airflow.tmp_supervisor_plant
;

DROP TABLE IF EXISTS airflow.tmp_supervisor_plant;
