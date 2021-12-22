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
    s.id,
    STAGED.question_id,
    STAGED.id
FROM
    airflow.answer_staged STAGED
    LEFT JOIN answer TARGET ON TARGET.source_id = STAGED.source_id
    INNER JOIN airflow.self_evaluation_staged se on se.id = STAGED.self_evaluation_id
    INNER JOIN self_evaluation s on se.source_id = s.source_id
WHERE STAGED.job_id = %(job_id)s :: BIGINT
    AND TARGET.id IS NULL
;

UPDATE
    answer TARGET
SET
    values = STAGED.values,
    attachments = STAGED.attachments,
    observations = STAGED.observations,
    self_evaluation_id = se.id,
    question_id = q.id
FROM
    airflow.answer_staged STAGED,
    airflow.self_evaluation_staged ses,
    self_evaluation se,
    self_evaluation sse,
    airflow.question_staged qs,
    question q,
    question qq
WHERE
    STAGED.source_id = TARGET.source_id
    AND ses.id = STAGED.self_evaluation_id
    AND se.source_id = ses.source_id
    AND sse.id = TARGET.self_evaluation_id
    AND qs.id = STAGED.question_id
    AND q.source_id = qs.source_id
    AND qq.id = TARGET.question_id
    AND STAGED.job_id = %(job_id)s :: BIGINT
    AND (
        STAGED.values IS DISTINCT FROM TARGET.values OR
        STAGED.attachments IS DISTINCT FROM TARGET.attachments OR
        STAGED.observations IS DISTINCT FROM TARGET.observations OR
        se.id IS DISTINCT FROM sse.id OR
        q.id IS DISTINCT FROM qq.id
    );
