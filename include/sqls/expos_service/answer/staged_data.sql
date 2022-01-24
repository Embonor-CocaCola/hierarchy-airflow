DELETE FROM
    airflow.answer_staged
WHERE
    job_id = %(job_id)s :: BIGINT;

INSERT INTO airflow.answer_staged (
    source_id,
    values,
    attachments,
    self_evaluation_id,
    question_id,

    created_at,
    updated_at,
    job_id
)
SELECT
    ANC.source_id,
    ANC.values,
    ANC.attachments,
    COALESCE(SE.id, ANC.self_evaluation_id),
    COALESCE(Q.id, QUC.id),

    now(),
    now(),
    ANC.job_id
FROM
    airflow.answer_conform ANC
    INNER JOIN airflow.question_conform QUC ON QUC.id = ANC.question_id :: uuid
    LEFT JOIN question Q on Q.source_id = QUC.source_id
    INNER JOIN airflow.self_evaluation_conform SEC ON SEC.id = ANC.self_evaluation_id
    LEFT JOIN self_evaluation SE on SE.source_id = SEC.source_id

WHERE ANC.job_id = %(job_id)s :: BIGINT
    AND QUC.job_id = %(job_id)s :: BIGINT
;
