DELETE FROM
    airflow.vendor_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_typed (
    source_id,
    name,
    rut,
    email,
    phone,
    branch_office,
    vendor_type_id,
    operation_range,
    deleted_at,
    driver_helper_code,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(source_id) :: INTEGER,
    trim(name),
    trim(rut)::int::text, -- To eliminate leading zeros
    trim(email),
    trim(phone),
    trim(branch_office) :: INTEGER,
    trim(vendor_type_id) :: INTEGER,
    trim(operation_range),
    to_timestamp(deleted_at, 'YYYY-MM-DD HH24:MI:SS'),
    trim(driver_helper_code),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_raw
WHERE job_id = %(job_id)s :: BIGINT
;
