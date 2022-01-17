DELETE FROM
    airflow.vendor_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_staged (
    source_id,
    name,
    rut,
    email,
    phone,
    branch_office_id,
    vendor_type,
    deleted_at,
    plant_id,
    supervisor_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    VEC.source_id,
    VPC.vendor_name,
    VEC.rut,
    VEC.email,
    VEC.phone,
    COALESCE(b.id, BOC.id),
    VTC.name,
    VEC.deleted_at,
    VPC.plant_id,
    VPC.supervisor_id,

    now(),
    now(),
    VEC.job_id,
    VEC.id
FROM
    airflow.vendor_conform VEC
    INNER JOIN airflow.branch_office_conform BOC ON BOC.source_id = VEC.branch_office_id
    LEFT JOIN branch_office b ON BOC.source_id = b.source_id
    INNER JOIN airflow.vendor_type_conform VTC ON VTC.source_id = VEC.vendor_type_id
    INNER JOIN airflow.vendor_plant_conform VPC ON substr(VEC.rut, 1, length(COALESCE(NULLIF(VEC.rut, ''), ' ')) - 1) = VPC.vendor_id :: TEXT
WHERE
    VEC.job_id = %(job_id)s :: BIGINT AND
    BOC.job_id = %(job_id)s :: BIGINT AND
    VTC.job_id = %(job_id)s :: BIGINT AND
    VPC.job_id = %(job_id)s :: BIGINT
;
