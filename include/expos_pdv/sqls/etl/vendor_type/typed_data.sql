DELETE FROM
    airflow.vendor_type_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_type_typed (
    source_id,
    name,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(source_id) :: INTEGER,
    trim(name),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_type_raw
WHERE job_id = %(job_id)s :: BIGINT
;
