DELETE FROM
    airflow.vendor_plant_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_plant_typed (
    vendor_id,
    supervisor_id,
    chief_rut,
    plant_id,
    vendor_name,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim(vendor_id) :: INTEGER,
    trim(supervisor_id) :: INTEGER,
    trim(chief_rut),
    trim(plant_id) :: INTEGER,
    trim(vendor_name),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.vendor_plant_raw
WHERE job_id = %(job_id)s :: BIGINT
AND supervisor_id IS NOT NULL
;



INSERT INTO airflow.vendor_plant_typed (
    vendor_id,
    supervisor_id,
    chief_rut,
    plant_id,
    vendor_name,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    substr(trim(tmh.vendor_rut), 1, length(COALESCE(NULLIF(tmh.vendor_rut, ''), ' ')) - 1)::int,
    substr(trim(tmh.supervisor_rut), 1, length(COALESCE(NULLIF(tmh.supervisor_rut, ''), ' ')) - 1)::int,
    '99999999',
    br.plant_id :: int,
    initcap(trim(vr.name)),

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()
FROM
    airflow.tmp_missing_hierarchy tmh
    INNER JOIN airflow.vendor_raw vr ON vr.rut ~ ('^[0]?' || tmh.vendor_rut || '$')
    INNER JOIN airflow.branch_office_raw br on vr.branch_office = br.source_id
WHERE
    vr.job_id = %(job_id)s :: BIGINT AND
    br.job_id = %(job_id)s :: BIGINT
;
