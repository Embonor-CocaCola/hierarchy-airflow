INSERT INTO branch_office (
    source_id,
    name,
    plant_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.name,
    STAGED.plant_id,
    STAGED.id
FROM
    airflow.branch_office_staged STAGED
LEFT JOIN branch_office TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    branch_office TARGET
SET
    name = STAGED.name,
    plant_id = pp.id
FROM
    airflow.branch_office_staged STAGED,
    branch_office bo,
    airflow.plant_staged pls,
    plant p,
    plant pp
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.source_id = bo.source_id
    AND pls.id = STAGED.plant_id
    AND bo.plant_id = p.id
    AND pls.source_id = pp.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name OR
        p.source_id IS DISTINCT FROM pp.source_id
    );
