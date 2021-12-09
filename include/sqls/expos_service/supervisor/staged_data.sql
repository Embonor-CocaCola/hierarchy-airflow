DELETE FROM
    airflow.supervisor_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.supervisor_staged (
    source_id,
    name,
    plant_id,
    code,
    location,
    role,
    chief_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    SUC.source_id,
    SUC.name,
    PLC.id,
    SUC.code,
    SUC.location,
    SUC.role,
    CHC.id ,

    now(),
    now(),
    SUC.job_id,
    SUC.id
FROM
    airflow.supervisor_conform SUC
INNER JOIN airflow.chief_conform CHC ON CHC.source_id = SUC.chief_id
INNER JOIN airflow.plant_conform PLC ON PLC.source_id = SUC.plant_id

WHERE SUC.job_id = %(job_id)s :: BIGINT
    AND CHC.job_id = %(job_id)s :: BIGINT
    AND PLC.job_id = %(job_id)s :: BIGINT
;
