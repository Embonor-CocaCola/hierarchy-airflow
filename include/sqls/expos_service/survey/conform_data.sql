DELETE FROM
    airflow.survey_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.survey_conform (
    source_id,
    source_survey_id,
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
    source_id,
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
