DELETE FROM
    airflow.self_evaluation_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.self_evaluation_staged (
    source_id,
    skips_survey,
    vendor_id,
    customer_id,
    external_created_at,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    SEC.source_id,
    SEC.skips_survey,
    v.id,
    c.id,
    SEC.external_created_at,

    now(),
    now(),
    SEC.job_id,
    SEC.id
FROM
    airflow.self_evaluation_conform SEC
    INNER JOIN airflow.vendor_conform VEC ON VEC.source_id = SEC.vendor_id
    INNER JOIN vendor v ON VEC.source_id = v.source_id
    INNER JOIN airflow.customer_conform CUC ON CUC.source_id = SEC.customer_id
    INNER JOIN customer c ON CUC.source_id = c.source_id
WHERE
    SEC.job_id = %(job_id)s :: BIGINT AND
    VEC.job_id = %(job_id)s :: BIGINT AND
    CUC.job_id = %(job_id)s :: BIGINT
;
