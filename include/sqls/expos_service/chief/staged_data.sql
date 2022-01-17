DELETE FROM
    airflow.chief_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.chief_staged (
    source_id,
    name,
    plant_id,
    code,
    location,
    rut,
    role,
    unit,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    CHC.source_id,
    CHC.name,
    COALESCE(p.id, PLC.id),
    CHC.code,
    CHC.location,
    CHC.rut,
    CHC.role,
    CHC.unit,

    now(),
    now(),
    CHC.job_id,
    CHC.id
FROM
    airflow.chief_conform CHC
    INNER JOIN airflow.plant_conform PLC ON PLC.source_id = CHC.plant_id
    LEFT JOIN plant p ON PLC.source_id = p.source_id
WHERE CHC.job_id = %(job_id)s :: BIGINT
    AND PLC.job_id = %(job_id)s :: BIGINT
;
