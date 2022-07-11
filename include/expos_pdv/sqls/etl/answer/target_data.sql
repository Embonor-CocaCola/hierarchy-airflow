INSERT INTO answer (
    source_id,
    values,
    attachments,
    observations,
    survey_id,
    question_id,
    id
)
SELECT
    STAGED.source_id,
    STAGED.values,
    STAGED.attachments,
    STAGED.observations,
    STAGED.survey_id,
    STAGED.question_id,
    STAGED.id
FROM
    airflow.answer_staged STAGED
    INNER JOIN survey se ON STAGED.survey_id = se.id
    LEFT JOIN answer TARGET ON TARGET.source_id = STAGED.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

ANALYZE answer;

UPDATE
    answer TARGET
SET
    values = STAGED.values,
    attachments = STAGED.attachments,
    observations = STAGED.observations,
    survey_id = sse.id,
    question_id = STAGED.question_id
FROM
    airflow.answer_staged STAGED,
    airflow.survey_staged ses,
    survey se,
    survey sse
WHERE
    STAGED.source_id = TARGET.source_id
    AND ses.id = STAGED.survey_id
    AND se.id = TARGET.survey_id
    AND sse.source_id = se.source_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND ses.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.values IS DISTINCT FROM TARGET.values OR
        STAGED.attachments IS DISTINCT FROM TARGET.attachments OR
        STAGED.observations IS DISTINCT FROM TARGET.observations OR
        se.id IS DISTINCT FROM sse.id OR
        STAGED.question_id IS DISTINCT FROM TARGET.question_id
    );

ANALYZE answer;
