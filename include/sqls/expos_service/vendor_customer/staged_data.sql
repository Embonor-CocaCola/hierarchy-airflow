DELETE FROM
    airflow.vendor_customer_staged
WHERE
    job_id = %(job_id)s :: BIGINT;
ANALYZE (SKIP_LOCKED, VERBOSE) airflow.vendor_customer_staged;

INSERT INTO airflow.vendor_customer_staged (
    vendor_id,
    customer_id,
    start_date,
    frequency,
    priority,

    created_at,
    updated_at,
    job_id,
    id,
    target_id
)
SELECT
    COALESCE(v.id, VEC.id),
    COALESCE(c.id, CUC.id),
    VCC.start_date,
    VCC.frequency,
    VCC.priority,

    now(),
    now(),
    VCC.job_id,
    VCC.id,
    VCC.target_id
FROM
    airflow.vendor_customer_conform VCC
    INNER JOIN airflow.customer_conform CUC ON CUC.source_id = VCC.customer_id
    LEFT JOIN customer c ON CUC.source_id = c.source_id
    INNER JOIN airflow.vendor_conform VEC ON VEC.source_id = VCC.vendor_id
    LEFT JOIN vendor v ON VEC.source_id = v.source_id
WHERE
    VCC.job_id = %(job_id)s :: BIGINT AND
    CUC.job_id = %(job_id)s :: BIGINT AND
    VEC.job_id = %(job_id)s :: BIGINT
;
