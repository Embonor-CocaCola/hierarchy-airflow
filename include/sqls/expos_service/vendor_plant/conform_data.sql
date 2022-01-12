DELETE FROM
    airflow.vendor_plant_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.vendor_plant_conform (
    vendor_id,
    supervisor_id,
    plant_id,
    vendor_name,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    TVP.vendor_id,
    TSP.id,
    TPL.id,
    TVP.vendor_name,

    now(),
    now(),
    TVP.job_id,
    TVP.id
FROM
    airflow.vendor_plant_typed TVP
    LEFT JOIN airflow.plant_typed TPL ON TPL.source_id = TVP.plant_id
    LEFT JOIN airflow.supervisor_plant_typed TSP ON TSP.supervisor_id = TVP.supervisor_id
WHERE
    TVP.job_id = %(job_id)s :: BIGINT AND
    TPL.job_id = %(job_id)s :: BIGINT AND
    TSP.job_id = %(job_id)s :: BIGINT
;
