DELETE FROM
    airflow.plant_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.plant_raw (
    source_id,
    name,
    created_at,
    updated_at,
    job_id
)

SELECT
    id,
    name,
    now(),
    now(),
    %(job_id)s :: BIGINT
FROM
    airflow.tmp_plant
;

DROP TABLE IF EXISTS airflow.tmp_plant;
