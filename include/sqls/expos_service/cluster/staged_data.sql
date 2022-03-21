DELETE FROM
    airflow.cluster_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.cluster_staged (
    name,
    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    name,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.cluster_conform
WHERE job_id = %(job_id)s :: BIGINT
;
