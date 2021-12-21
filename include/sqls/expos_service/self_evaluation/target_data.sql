INSERT INTO self_evaluation (
    source_id,
    skips_survey,
    vendor_id,
    customer_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.skips_survey,
    STAGED.vendor_id,
    STAGED.customer_id,
    STAGED.id
FROM
    airflow.self_evaluation_staged STAGED
-- TODO: Inner Joins below make sure that we don't attempt to insert rows without foreign related rows
-- Before going into prod, we must add another query to do the inverse and store the
-- rows with missing relation in an error table to do notifying and other handling logic
INNER JOIN vendor VES ON VES.id = STAGED.vendor_id
LEFT JOIN self_evaluation TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    self_evaluation TARGET
SET
    skips_survey = STAGED.skips_survey,
    vendor_id = STAGED.vendor_id,
    customer_id = STAGED.customer_id
FROM
    airflow.self_evaluation_staged STAGED
    INNER JOIN vendor VES ON VES.id = STAGED.vendor_id
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.skips_survey IS DISTINCT FROM TARGET.skips_survey OR
        STAGED.vendor_id IS DISTINCT FROM TARGET.vendor_id OR
        STAGED.customer_id IS DISTINCT FROM TARGET.customer_id
    );
