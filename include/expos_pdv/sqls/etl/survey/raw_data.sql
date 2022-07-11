DELETE FROM
    airflow.survey_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.survey_raw (
    source_id,
    name,
    paused,
    portals,
    valid_since,
    valid_until,
    external_created_at,
    external_updated_at,

    created_at,
    updated_at,
    job_id,
    id
)

SELECT
    id,
    name,
    paused,
    portals,
    valid_since,
    valid_until,
    created_at,
    updated_at,

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()
FROM
    airflow.tmp_survey
WHERE name = 'Autoevaluación'
;

DROP TABLE IF EXISTS airflow.tmp_survey;
