INSERT INTO self_evaluation (
    source_id,
    skips_survey,
    vendor_id,
    customer_id,
    created_at,
    id
)
SELECT
    STAGED.source_id,
    STAGED.skips_survey,
    STAGED.vendor_id,
    STAGED.customer_id,
    STAGED.external_created_at,
    STAGED.id
FROM
    airflow.self_evaluation_staged STAGED
-- TODO: Inner Joins below make sure that we don't attempt to insert rows without foreign related rows
-- Before going into prod, we must add another query to do the inverse and store the
-- rows with missing relation in an error table to do notifying and other handling logic
INNER JOIN airflow.vendor_staged vs ON vs.id = STAGED.vendor_id
INNER JOIN airflow.customer_staged cs ON cs.id = STAGED.customer_id
INNER JOIN vendor v ON v.source_id = vs.source_id
INNER JOIN customer c ON c.source_id = cs.source_id
LEFT JOIN self_evaluation TARGET ON TARGET.source_id = STAGED.source_id
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND cs.job_id = %(job_id)s :: BIGINT
    AND vs.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    self_evaluation TARGET
SET
    skips_survey = STAGED.skips_survey,
    created_at = STAGED.external_created_at,
    vendor_id = v.id,
    customer_id = c.id
FROM
    airflow.self_evaluation_staged STAGED,
    airflow.vendor_staged vs,
    vendor v,
    vendor vv,
    airflow.customer_staged cs,
    customer c,
    customer cc
WHERE
    vs.id = STAGED.vendor_id
    AND v.source_id = vs.source_id
    AND vv.id = TARGET.vendor_id
    AND cs.id = STAGED.customer_id
    AND c.source_id = cs.source_id
    AND cc.id = TARGET.customer_id
    AND STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND vs.job_id = %(job_id)s :: BIGINT
    AND cs.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.skips_survey IS DISTINCT FROM TARGET.skips_survey OR
        STAGED.external_created_at IS DISTINCT FROM TARGET.created_at OR
        v.id IS DISTINCT FROM vv.id OR
        c.id IS DISTINCT FROM cc.id
    );

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
