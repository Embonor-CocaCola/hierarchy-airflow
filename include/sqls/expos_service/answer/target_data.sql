INSERT INTO answer (
    source_id,
    values,
    attachments,
    observations,
    self_evaluation_id,
    question_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.values,
    STAGED.attachments,
    STAGED.observations,
    STAGED.self_evaluation_id,
    STAGED.question_id,
    STAGED.id
FROM
    airflow.answer_staged STAGED
LEFT JOIN answer TARGET ON TARGET.id = STAGED.id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    answer TARGET
SET
    values = STAGED.values,
    attachments = STAGED.attachments,
    observations = STAGED.observations,
    self_evaluation_id = STAGED.self_evaluation_id,
    question_id = STAGED.question_id
FROM
    airflow.answer_staged STAGED
WHERE
    STAGED.source_id = TARGET.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.values IS DISTINCT FROM TARGET.values OR
        STAGED.attachments IS DISTINCT FROM TARGET.attachments OR
        STAGED.observations IS DISTINCT FROM TARGET.observations OR
        STAGED.self_evaluation_id IS DISTINCT FROM TARGET.self_evaluation_id OR
        STAGED.question_id IS DISTINCT FROM TARGET.question_id
    );
