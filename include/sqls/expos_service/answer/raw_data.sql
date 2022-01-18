DELETE FROM
    airflow.answer_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.answer_raw (
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
    job_id
)
SELECT
    id,
    surveyid,
    latitude,
    longitude,
    skipssurvey,
    pollsterid,
    surveyedid,
    createdat,
    regexp_replace(answers, '\\u0000', '', 'g'),

    now(),
    now(),
    %(job_id)s :: BIGINT
FROM
    airflow.tmp_answer
;

DROP TABLE IF EXISTS airflow.tmp_answer;
