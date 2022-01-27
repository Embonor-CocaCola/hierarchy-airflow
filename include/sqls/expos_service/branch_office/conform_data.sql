DELETE FROM
    airflow.branch_office_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

ANALYZE airflow.branch_office_conform;

INSERT INTO airflow.branch_office_conform (
    source_id,
    name,
    plant_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    source_id,
    name,
    plant_id,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.branch_office_typed
WHERE job_id = %(job_id)s :: BIGINT
;

ANALYZE airflow.branch_office_conform;
