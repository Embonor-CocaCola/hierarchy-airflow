INSERT INTO supervisor (
    source_id,
    name,
    code,
    location,
    chief_id,
    role,

    plant_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.name,
    STAGED.code,
    STAGED.location,
    STAGED.chief_id,
    STAGED.role,

    STAGED.plant_id,
    STAGED.id
FROM
    airflow.supervisor_staged STAGED
LEFT JOIN supervisor TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;


ANALYZE supervisor;
UPDATE
    supervisor TARGET
SET
    name = STAGED.name,
    code = STAGED.code,
    location = STAGED.location,
    chief_id = STAGED.chief_id,
    role = STAGED.role,
    plant_id = STAGED.plant_id
FROM
    airflow.supervisor_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name OR
        STAGED.code IS DISTINCT FROM TARGET.code OR
        STAGED.location IS DISTINCT FROM TARGET.location OR
        STAGED.chief_id IS DISTINCT FROM TARGET.chief_id OR
        STAGED.role IS DISTINCT FROM TARGET.role OR
        STAGED.plant_id IS DISTINCT FROM TARGET.plant_id)
;
ANALYZE supervisor;
