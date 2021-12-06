DELETE FROM
    airflow.self_evaluation_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.self_evaluation_conform (
    source_id,
    skips_survey,
    vendor_id,
    customer_id,
    external_created_at,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    survey_id,
    skips_survey,
    pollster_id,
    surveyed_id,
    external_created_at,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.answer_typed
WHERE job_id = %(job_id)s :: BIGINT
;
