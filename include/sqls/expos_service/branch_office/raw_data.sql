DELETE FROM
    airflow.branch_office_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

ANALYZE airflow.branch_office_raw;

INSERT INTO airflow.branch_office_raw (
    source_id,
    name,
    plant_id,
    created_at,
    updated_at,
    job_id
)

SELECT
    id,
    name,
    plantId,
    now(),
    now(),
    %(job_id)s :: BIGINT
FROM
    airflow.tmp_branch_office
;

ANALYZE airflow.branch_office_raw;

DROP TABLE IF EXISTS airflow.tmp_branch_office;
