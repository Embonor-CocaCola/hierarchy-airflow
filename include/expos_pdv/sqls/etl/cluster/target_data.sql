INSERT INTO cluster (
    name,
    id
)
SELECT
    STAGED.name,
    STAGED.id
FROM
    airflow.cluster_staged STAGED
LEFT JOIN cluster TARGET ON TARGET.name = STAGED.name
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;
