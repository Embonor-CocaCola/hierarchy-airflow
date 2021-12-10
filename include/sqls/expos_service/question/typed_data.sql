DELETE FROM
    airflow.question_typed
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.question_typed (
    source_id,
    attach,
    heading,
    options,
    type,
    sub_type,
    external_created_at,
    external_updated_at,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    trim((source_id:: jsonb)->>'$oid'),
    trim(attach) :: jsonb,
    trim(heading),
    trim(options) :: jsonb,
    trim(type),
    trim(sub_type),
    to_timestamp(((external_created_at :: jsonb)->>'$date') {{ params.date_cast }}),
    to_timestamp(((external_updated_at :: jsonb)->>'$date') {{ params.date_cast }}),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.question_raw
WHERE job_id = %(job_id)s :: BIGINT
;
