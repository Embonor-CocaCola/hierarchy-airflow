DELETE FROM
    airflow.vendor_customer_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_customer_staged (
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
SELECT DISTINCT ON (VEC.id, CUC.id)
    VEC.id,
    CUC.id,
    VCC.start_date,
    VCC.frequency,
    VCC.priority,

    now(),
    now(),
    VCC.job_id,
    VCC.id
FROM
    airflow.vendor_customer_conform VCC
    INNER JOIN airflow.customer_conform CUC ON CUC.source_id = VCC.customer_id
    INNER JOIN airflow.vendor_conform VEC ON VEC.source_id = VCC.vendor_id
WHERE
    VCC.job_id = %(job_id)s :: BIGINT AND
    CUC.job_id = %(job_id)s :: BIGINT AND
    VEC.job_id = %(job_id)s :: BIGINT
;
