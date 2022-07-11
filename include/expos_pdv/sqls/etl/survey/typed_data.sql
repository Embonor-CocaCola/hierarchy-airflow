

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
    stringify_oid(trim(source_id)),
    trim(name),
    trim(paused) :: BOOLEAN,
    clean_survey_collection_ids(trim(portals) :: jsonb),
    to_timestamp(((valid_since :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
    to_timestamp(((valid_until :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
    to_timestamp(((external_created_at :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
    to_timestamp(((external_updated_at :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.survey_raw
WHERE job_id = %(job_id)s :: BIGINT
;
