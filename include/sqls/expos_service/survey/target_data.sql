INSERT INTO survey (
    source_id,
    skips_survey,
    vendor_id,
    customer_id,
    created_at,
    evaluation_status_id,
    id
)
SELECT
    STAGED.source_id,
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
    customer_id = STAGED.customer_id
FROM
    airflow.survey_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.external_created_at IS DISTINCT FROM TARGET.created_at OR
        STAGED.vendor_id IS DISTINCT FROM TARGET.vendor_id OR
        STAGED.customer_id IS DISTINCT FROM TARGET.customer_id
    );
ANALYZE survey;

UPDATE survey TARGET
SET
    skip_reason = CASE
                    WHEN ans.values->>0 LIKE '%%encuentra con reja' THEN 'gated'
                    WHEN ans.values->>0 LIKE '%%encuentra cerrado' THEN 'closed'
                    ELSE 'INVALID_REASON'
                END,
    skips_survey = true
FROM
    answer ans
WHERE
    ans.survey_id = TARGET.id
    AND TARGET.skip_reason IS NULL
    AND (
        ans.values->>0 LIKE '%%encuentra con reja' OR
        ans.values->>0 LIKE '%%encuentra cerrado'
    )
;
ANALYZE survey;
