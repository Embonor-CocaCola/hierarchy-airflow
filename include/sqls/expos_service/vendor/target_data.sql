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
    branch_office_id = bbo.id,
    vendor_type = STAGED.vendor_type,
    plant_id = pp.id,
    supervisor_id = ss.id,
    deleted_at = STAGED.deleted_at
FROM
    airflow.vendor_staged STAGED,
    vendor v,
    airflow.branch_office_staged bos,
    branch_office bo,
    branch_office bbo,
    airflow.plant_staged pls,
    plant p,
    plant pp,
    airflow.supervisor_staged sus,
    supervisor s,
    supervisor ss
WHERE
    STAGED.job_id = %(job_id)s :: BIGINT
    AND STAGED.source_id = v.source_id
    AND bos.id = STAGED.branch_office_id
    AND bo.id = v.branch_office_id
    AND bbo.source_id = bos.source_id
    AND pls.id = STAGED.plant_id
    AND p.id = v.plant_id
    AND pp.source_id = pls.source_id
    AND STAGED.supervisor_id = sus.id
    AND v.supervisor_id = s.id
    AND ss.source_id = sus.source_id
    AND pls.job_id = %(job_id)s :: BIGINT
    AND bos.job_id = %(job_id)s :: BIGINT
    AND sus.job_id = %(job_id)s :: BIGINT
    AND (
       STAGED.name IS DISTINCT FROM v.name OR
        STAGED.email IS DISTINCT FROM v.email OR
        STAGED.phone IS DISTINCT FROM v.phone OR
        STAGED.rut IS DISTINCT FROM v.rut OR
        bbo.source_id IS DISTINCT FROM bo.source_id OR
        STAGED.vendor_type IS DISTINCT FROM v.vendor_type OR
        pp.source_id IS DISTINCT FROM p.source_id OR
        ss.source_id IS DISTINCT FROM s.source_id OR
        STAGED.deleted_at IS DISTINCT FROM v.deleted_at)
;
