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

UPDATE
    supervisor TARGET
SET
    name = STAGED.name,
    code = STAGED.code,
    location = STAGED.location,
    chief_id = cc.id,
    role = STAGED.role,
    plant_id = pp.id
FROM
    airflow.supervisor_staged STAGED,
    supervisor s,
    airflow.plant_staged pls,
    plant p,
    plant pp,
    airflow.chief_staged cs,
    chief c,
    chief cc
WHERE
    STAGED.source_id = TARGET.source_id
    AND s.source_id = STAGED.source_id
    AND pls.id = STAGED.plant_id
    AND s.plant_id = p.id
    AND pls.source_id = pp.source_id
    AND cs.id = STAGED.chief_id
    AND s.chief_id = c.id
    AND  cs.source_id = cc.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND pls.job_id = %(job_id)s :: BIGINT
    AND cs.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM s.name OR
        STAGED.code IS DISTINCT FROM s.code OR
        STAGED.location IS DISTINCT FROM s.location OR
        cs.source_id IS DISTINCT FROM c.source_id OR
        STAGED.role IS DISTINCT FROM s.role OR
        pls.source_id IS DISTINCT FROM p.source_id)
;
