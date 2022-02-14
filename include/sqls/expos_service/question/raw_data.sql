DELETE FROM
    airflow.question_raw
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.question_raw (
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
    id,
    attach,
    heading,
    options,
    type,
    subtype,
    createdat,
    updatedat,

    now(),
    now(),
    %(job_id)s :: BIGINT,
    uuid_generate_v4()
FROM
    airflow.tmp_question
;

DROP TABLE IF EXISTS airflow.tmp_question;
