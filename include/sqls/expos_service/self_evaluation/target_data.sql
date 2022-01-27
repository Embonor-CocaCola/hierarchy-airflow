INSERT INTO self_evaluation (
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
    airflow.self_evaluation_staged STAGED
INNER JOIN airflow.vendor_staged VES on STAGED.vendor_id = VES.id
INNER JOIN airflow.customer_staged CUS on STAGED.customer_id = CUS.id
LEFT JOIN self_evaluation TARGET ON TARGET.source_id = STAGED.source_id
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND VES.job_id = %(job_id)s :: BIGINT
    AND CUS.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;
ANALYZE self_evaluation;

INSERT INTO airflow.self_evaluation_failed (
    source_id,
    vendor_source_id,
    customer_source_id,
    vendor_name,
    customer_name,

    job_id,
    created_at,
    updated_at
)
SELECT
    STAGED.source_id,
    VES.source_id,
    CUS.source_id,
    VES.name,
    CUS.name,

    STAGED.job_id,
    now(),
    now()
FROM
    airflow.self_evaluation_staged STAGED
LEFT JOIN airflow.vendor_staged VES on STAGED.vendor_id = VES.id
LEFT JOIN airflow.customer_staged CUS on STAGED.customer_id = CUS.id
LEFT JOIN self_evaluation TARGET ON TARGET.source_id = STAGED.source_id

WHERE (VES.id IS NULL OR CUS.id IS NULL)
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND VES.job_id = %(job_id)s :: BIGINT
    AND CUS.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

ANALYZE airflow.self_evaluation_failed;

UPDATE
    self_evaluation TARGET
SET
    created_at = STAGED.external_created_at,
    vendor_id = STAGED.vendor_id,
    customer_id = STAGED.customer_id
FROM
    airflow.self_evaluation_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.external_created_at IS DISTINCT FROM TARGET.created_at OR
        STAGED.vendor_id IS DISTINCT FROM TARGET.vendor_id OR
        STAGED.customer_id IS DISTINCT FROM TARGET.customer_id
    );
ANALYZE self_evaluation;

UPDATE self_evaluation TARGET
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
    ans.self_evaluation_id = TARGET.id
    AND TARGET.skip_reason IS NULL
    AND (
        ans.values->>0 LIKE '%%encuentra con reja' OR
        ans.values->>0 LIKE '%%encuentra cerrado'
    )
;
ANALYZE self_evaluation;
