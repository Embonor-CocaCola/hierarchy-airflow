DELETE FROM
    airflow.vendor_customer_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_customer_typed (
    vendor_id,
    customer_id,
    start_date,
    frequency,
    priority,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(vendor_id) :: INTEGER,
    trim(customer_id) :: INTEGER,
    to_timestamp(start_date, 'YYYY-MM-DD HH24:MI:SS'),
    trim(frequency) :: INTEGER,
    trim(priority) :: INTEGER,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_customer_raw
WHERE job_id = %(job_id)s :: BIGINT
;
