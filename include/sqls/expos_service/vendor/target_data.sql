INSERT INTO vendor (
    source_id,
    name,
    email,
    phone,
    rut,
    branch_office_id,
    vendor_type,
    plant_id,
    supervisor_id,
    deleted_at,
    id
)
SELECT
    STAGED.source_id,
    STAGED.name,
    STAGED.email,
    STAGED.phone,
    STAGED.rut,
    STAGED.branch_office_id,
    STAGED.vendor_type,
    STAGED.plant_id,
    STAGED.supervisor_id,
    STAGED.deleted_at,
    STAGED.id
FROM
    airflow.vendor_staged STAGED
INNER JOIN airflow.supervisor_staged SUS ON SUS.id = STAGED.supervisor_id
LEFT JOIN vendor TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    vendor TARGET
SET
    name = STAGED.name,
    email = STAGED.email,
    phone = STAGED.phone,
    rut = STAGED.rut,
    branch_office_id = STAGED.branch_office_id,
    vendor_type = STAGED.vendor_type,
    plant_id = STAGED.plant_id,
    supervisor_id = STAGED.supervisor_id,
    deleted_at = STAGED.deleted_at
FROM
    airflow.vendor_staged STAGED
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND STAGED.source_id = TARGET.source_id
    AND (
        STAGED.name IS DISTINCT FROM TARGET.name OR
        STAGED.email IS DISTINCT FROM TARGET.email OR
        STAGED.phone IS DISTINCT FROM TARGET.phone OR
        STAGED.rut IS DISTINCT FROM TARGET.rut OR
        STAGED.branch_office_id IS DISTINCT FROM TARGET.branch_office_id OR
        STAGED.vendor_type IS DISTINCT FROM TARGET.vendor_type OR
        STAGED.plant_id IS DISTINCT FROM TARGET.plant_id OR
        STAGED.supervisor_id IS DISTINCT FROM TARGET.supervisor_id OR
        STAGED.deleted_at IS DISTINCT FROM TARGET.deleted_at)
;
