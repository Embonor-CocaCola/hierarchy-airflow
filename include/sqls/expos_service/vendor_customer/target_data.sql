INSERT INTO vendor_customer (
    vendor_id,
    customer_id,
    start_date,
    id
)

(SELECT
    VCS.vendor_id,
    VCS.customer_id,
    VCS.start_date,
    VCS.target_id
FROM
    airflow.vendor_customer_staged VCS

-- TODO: Inner Joins below make sure that we don't attempt to insert rows without foreign related rows
-- Before going into prod, we must add another query to do the inverse and store the
-- rows with missing relation in an error table to do notifying and other handling logic
INNER JOIN customer CUS ON CUS.id = VCS.customer_id
INNER JOIN vendor VET ON VET.id = VCS.vendor_id
LEFT JOIN vendor_customer TARGET ON TARGET.id = VCS.target_id
WHERE VCS.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL)
;
ANALYZE vendor_customer;

DELETE FROM
    vendor_customer TARGET
WHERE
    TARGET.id IN (
            SELECT VC.id FROM vendor_customer VC
                LEFT JOIN airflow.vendor_customer_staged VCS
                ON VCS.target_id = VC.id
                WHERE VCS.target_id IS NULL
        )
;
ANALYZE vendor_customer;
