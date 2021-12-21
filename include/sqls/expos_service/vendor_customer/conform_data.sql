DELETE FROM
    airflow.vendor_customer_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_customer_conform (
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
    vendor_id,
    customer_id,
    start_date,
    frequency,
    priority,

    now(),
    now(),
    job_id,
    CONCAT(vendor_id :: TEXT, customer_id :: TEXT, extract(epoch from start_date) :: TEXT)
FROM
    airflow.vendor_customer_typed
WHERE job_id = %(job_id)s :: BIGINT
;
