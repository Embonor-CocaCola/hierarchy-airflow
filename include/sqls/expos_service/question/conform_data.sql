DELETE FROM
    airflow.question_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.question_conform (
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
    source_id,
    attach,
    heading,
    options,
    type,
    sub_type,
    external_created_at,
    external_updated_at,

    now(),
    now(),
    job_id,
    id
FROM
    airflow.question_typed
WHERE job_id = %(job_id)s :: BIGINT
;
