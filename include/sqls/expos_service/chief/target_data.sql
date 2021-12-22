INSERT INTO chief (
    source_id,
    name,
    code,
    location,
    rut,
    role,
    unit,
    plant_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.name,
    STAGED.code,
    STAGED.location,
    STAGED.rut,
    STAGED.role,
    STAGED.unit,
    STAGED.plant_id,
    STAGED.id
FROM
    airflow.chief_staged STAGED
LEFT JOIN chief TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    chief TARGET
SET
    name = STAGED.name,
    code = STAGED.code,
    location = STAGED.location,
    rut = STAGED.rut,
    role = STAGED.role,
    unit = STAGED.unit,
    plant_id = pp.id
FROM
    airflow.chief_staged STAGED,
    chief c,
    airflow.plant_staged pls,
    plant p,
    plant pp
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.source_id = c.source_id
    AND pls.id = STAGED.plant_id
    AND c.plant_id = p.id
    AND pls.source_id = pp.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name OR
        STAGED.code IS DISTINCT FROM TARGET.code OR
        STAGED.location IS DISTINCT FROM TARGET.location OR
        STAGED.rut IS DISTINCT FROM TARGET.rut OR
        STAGED.role IS DISTINCT FROM TARGET.role OR
        STAGED.unit IS DISTINCT FROM TARGET.unit OR
        pls.source_id IS DISTINCT FROM p.source_id)
;
