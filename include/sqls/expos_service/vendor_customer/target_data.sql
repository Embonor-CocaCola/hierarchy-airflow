INSERT INTO vendor_customer (
    vendor_id,
    customer_id
)

(SELECT
    VCS.vendor_id,
    VCS.customer_id
FROM
    airflow.vendor_customer_staged VCS
INNER JOIN airflow.customer_staged CUS ON CUS.id = VCS.customer_id
INNER JOIN vendor VET ON VET.id = VCS.vendor_id
LEFT JOIN vendor_customer TARGET ON TARGET.vendor_id = VCS.vendor_id AND TARGET.customer_id = VCS.customer_id
WHERE VCS.job_id = %(job_id)s :: BIGINT
    AND TARGET.vendor_id IS NULL)
ON CONFLICT (vendor_id, customer_id) DO NOTHING
;

UPDATE
    vendor_customer TARGET
SET
    vendor_id = STAGED.vendor_id,
    customer_id = STAGED.customer_id
FROM
    airflow.vendor_customer_staged STAGED
WHERE
    STAGED.vendor_id = TARGET.vendor_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.vendor_id IS DISTINCT FROM TARGET.vendor_id OR
        STAGED.customer_id IS DISTINCT FROM TARGET.customer_id
)
;
