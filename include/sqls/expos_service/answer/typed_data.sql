DELETE FROM
    airflow.answer_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.answer_typed (
    source_id,
    survey_id,
    latitude,
    longitude,
    skips_survey,
    pollster_id,
    surveyed_id,
    external_created_at,
    answers,
    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim((source_id:: jsonb)->>'$oid'),
    trim(survey_id),
    trim(latitude) :: FLOAT,
    trim(longitude) :: FLOAT,
    CASE skips_survey
        WHEN '0' THEN false
        WHEN '1' THEN true
        ELSE false
        END,
    trim(pollster_id) :: INTEGER,
    trim(surveyed_id) :: INTEGER,
    to_timestamp(((external_created_at :: jsonb)->>'$date') {{ params.date_cast }}),
    clean_answer_collection_ids(trim(answers) :: jsonb),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.answer_raw
WHERE job_id = %(job_id)s :: BIGINT
;
