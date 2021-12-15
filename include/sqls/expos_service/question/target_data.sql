INSERT INTO question (
    source_id,
    heading,
    options,
    type,
    sub_type,
    id
)
SELECT
    STAGED.source_id,
    STAGED.heading,
    STAGED.options,
    STAGED.type,
    STAGED.sub_type,
    STAGED.id
FROM
    airflow.question_staged STAGED
LEFT JOIN question TARGET ON TARGET.id = STAGED.id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    question TARGET
SET
    heading = STAGED.heading,
    options = STAGED.options,
    type = STAGED.type,
    sub_type = STAGED.sub_type
FROM
    airflow.question_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.heading IS DISTINCT FROM TARGET.heading OR
        STAGED.options IS DISTINCT FROM TARGET.options OR
        STAGED.type IS DISTINCT FROM TARGET.type OR
        STAGED.sub_type IS DISTINCT FROM TARGET.sub_type
    );
