INSERT INTO plant (
    source_id,
    name,
    id
)
SELECT
    STAGED.source_id,
    STAGED.name,
    STAGED.id
FROM
    airflow.plant_staged STAGED
LEFT JOIN plant TARGET ON TARGET.id = STAGED.id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    plant TARGET
SET
    name = STAGED.name
FROM
    airflow.plant_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name
    );
