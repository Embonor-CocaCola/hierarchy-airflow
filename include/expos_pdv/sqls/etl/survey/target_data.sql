INSERT INTO survey (
    source_id,
    source_survey_id,
    skips_survey,
    vendor_id,
    customer_id,
    created_at,
    evaluation_status_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.source_survey_id,
    STAGED.skips_survey,
    STAGED.vendor_id,
    STAGED.customer_id,
    STAGED.external_created_at,
    (SELECT id FROM evaluation_status WHERE code = 'NS'), -- Not supervised by default
    STAGED.id
FROM
    airflow.survey_staged STAGED
    INNER JOIN customer c on STAGED.customer_id = c.id
    INNER JOIN vendor v on STAGED.vendor_id = v.id
LEFT JOIN survey TARGET ON TARGET.source_id = STAGED.source_id
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;
ANALYZE survey;

UPDATE
    survey TARGET
SET
    created_at = STAGED.external_created_at,
    vendor_id = STAGED.vendor_id,
    customer_id = STAGED.customer_id,
    source_survey_id = STAGED.source_survey_id
FROM
    airflow.survey_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.external_created_at IS DISTINCT FROM TARGET.created_at OR
        STAGED.vendor_id IS DISTINCT FROM TARGET.vendor_id OR
        STAGED.customer_id IS DISTINCT FROM TARGET.customer_id OR
        STAGED.source_survey_id IS DISTINCT FROM TARGET.source_survey_id
    );
ANALYZE survey;
