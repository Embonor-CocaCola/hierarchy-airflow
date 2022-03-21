DELETE FROM
    airflow.cluster_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.cluster_conform (
    name,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    distinct(COALESCE(country_specific->>'cluster', 'Sin cluster')),

    now(),
    now(),
    job_id,
    uuid_generate_v4()
FROM
    airflow.customer_typed
WHERE job_id = %(job_id)s :: BIGINT
;
