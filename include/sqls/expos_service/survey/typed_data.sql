

DELETE FROM
    airflow.survey_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.survey_typed (
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
    trim((source_id:: jsonb)->>'$oid'),
    trim(name),
    trim(paused) :: BOOLEAN,
    clean_survey_collection_ids(trim(portals) :: jsonb),
    to_timestamp(((valid_since :: jsonb)->>'$date') {{ params.date_cast }}),
    to_timestamp(((valid_until :: jsonb)->>'$date') {{ params.date_cast }}),
    to_timestamp(((external_created_at :: jsonb)->>'$date') {{ params.date_cast }}),
    to_timestamp(((external_updated_at :: jsonb)->>'$date') {{ params.date_cast }}),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.survey_raw
WHERE job_id = %(job_id)s :: BIGINT
;
