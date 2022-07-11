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
    stringify_oid(trim(source_id)),
    COALESCE(trim(attach), '[]') :: jsonb,
    trim(heading),
    trim(options) :: jsonb,
    trim(type),
    trim(sub_type),
    to_timestamp(((external_created_at :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),
    to_timestamp(((external_updated_at :: jsonb)->>'$date'), 'YYYY-MM-DD"T"HH24:MI:SS"Z"'),

    now(),
    now(),
    job_id,
    id
FROM
    airflow.question_raw
WHERE job_id = %(job_id)s :: BIGINT
;
