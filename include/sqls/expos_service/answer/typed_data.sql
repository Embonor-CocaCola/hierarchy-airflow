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
    trim((raw.source_id:: jsonb)->>'$oid'),
    trim(raw.survey_id),
    trim(raw.latitude) :: FLOAT,
    trim(raw.longitude) :: FLOAT,
    CASE raw.skips_survey
        WHEN '0' THEN false
        WHEN '1' THEN true
        ELSE false
        END,
    trim(raw.pollster_id) :: INTEGER,
    trim(raw.surveyed_id) :: INTEGER,
    to_timestamp(((raw.external_created_at :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
    clean_answer_collection_ids(trim(raw.answers) :: jsonb),

    now(),
    now(),
    raw.job_id,
    COALESCE(s.id, raw.id)
FROM
    airflow.answer_raw raw
LEFT JOIN public.self_evaluation s ON s.source_id = raw.source_id
WHERE job_id = %(job_id)s :: BIGINT
;
