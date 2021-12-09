DELETE FROM
    airflow.vendor_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_raw (
    source_id,
    name,
    rut,
    email,
    phone,
    branch_office,
    vendor_type_id,
    operation_range,
    deleted_at,
    driver_helper_code,

    created_at,
    updated_at,
    job_id
)

SELECT
    id,
    name,
    rut,
    email,
    phone,
    branchoffice,
    vendortypeid,
    operationrange,
    deletedat,
    driverhelpercode,

    now(),
    now(),
    %(job_id)s :: BIGINT
FROM
    airflow.tmp_vendor TMP
;

DROP TABLE IF EXISTS airflow.tmp_vendor;
