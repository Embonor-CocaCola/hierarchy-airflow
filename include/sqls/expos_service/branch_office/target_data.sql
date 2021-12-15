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
LEFT JOIN branch_office TARGET ON TARGET.id = STAGED.id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    branch_office TARGET
SET
    name = STAGED.name,
    plant_id = STAGED.plant_id
FROM
    airflow.branch_office_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name OR
        STAGED.plant_id IS DISTINCT FROM TARGET.plant_id
    );
