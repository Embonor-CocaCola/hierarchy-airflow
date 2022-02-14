DELETE FROM
    airflow.answer_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

ANALYZE airflow.answer_staged;

INSERT INTO airflow.answer_staged (
    source_id,
    values,
    attachments,
    survey_id,
    question_id,

    created_at,
    updated_at,
    job_id,
    id
)
SELECT
    ANC.source_id,
    ANC.values,
    ANC.attachments,
    COALESCE(SE.id, ANC.survey_id),
    COALESCE(Q.id, QUC.id),

    now(),
    now(),
    ANC.job_id,
    ANC.id
FROM
    airflow.answer_conform ANC
    INNER JOIN airflow.question_conform QUC ON QUC.id = ANC.question_id :: uuid
    LEFT JOIN question Q on Q.source_id = QUC.source_id
    INNER JOIN airflow.survey_conform SEC ON SEC.id = ANC.survey_id
    LEFT JOIN survey SE on SE.source_id = SEC.source_id

WHERE ANC.job_id = %(job_id)s :: BIGINT
    AND QUC.job_id = %(job_id)s :: BIGINT
;
