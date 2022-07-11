DELETE FROM
    airflow.vendor_type_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_type_conform (
    source_id,
    name,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    source_id,
    name,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_type_typed
WHERE job_id = %(job_id)s :: BIGINT
;
