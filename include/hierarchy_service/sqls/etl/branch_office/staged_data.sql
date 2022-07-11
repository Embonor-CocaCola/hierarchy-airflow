DELETE FROM
    airflow.branch_office_staged
WHERE
    job_id = %(job_id)s :: BIGINT;
ANALYZE airflow.branch_office_staged;

INSERT INTO airflow.branch_office_staged (
    source_id,
    name,
    plant_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    BOC.source_id,
    BOC.name,
    COALESCE(p.id, PLC.id),

    now(),
    now(),
    BOC.job_id,
    BOC.id
FROM
    airflow.branch_office_conform BOC
    INNER JOIN airflow.plant_conform PLC ON BOC.plant_id = PLC.source_id
    LEFT JOIN plant p on PLC.source_id = p.source_id
WHERE BOC.job_id = %(job_id)s :: BIGINT
    AND PLC.job_id = %(job_id)s :: BIGINT
;
ANALYZE airflow.branch_office_staged;
