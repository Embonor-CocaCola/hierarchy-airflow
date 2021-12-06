DELETE FROM
    airflow.vendor_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_conform (
    source_id,
    name,
    rut,
    email,
    phone,
    branch_office_id,
    vendor_type_id,
    deleted_at,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    source_id,
    name,
    rut,
    email,
    phone,
    branch_office,
    vendor_type_id,
    deleted_at,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_typed

WHERE
    job_id = %(job_id)s :: BIGINT
;
