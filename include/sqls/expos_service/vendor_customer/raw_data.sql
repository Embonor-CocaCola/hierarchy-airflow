DELETE FROM
    airflow.vendor_customer_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_customer_raw (
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
    vendorid,
    customerid,
    startdate,
    frequency,
    priority,

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()
FROM
    airflow.tmp_vendor_customer
{#ON CONFLICT ON CONSTRAINT#}
{#    vendor_customer_raw_uidx#}
{#DO NOTHING#}
;

DROP TABLE IF EXISTS airflow.tmp_vendor_customer;
