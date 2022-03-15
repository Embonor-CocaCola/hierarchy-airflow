DELETE FROM
    airflow.answer_conform
WHERE
    job_id = %(job_id)s :: BIGINT;

ANALYZE airflow.answer_conform;

INSERT INTO airflow.answer_conform (
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
    ANS->>'id',
    ANS->'value',
    ARRAY(SELECT jsonb_array_elements_text(ANS->'attach')),
    TYPED.id,
    find_question_id_from_portals(SUR.portals, ANS->>'questionId', %(job_id)s::INTEGER),

    now(),
    now(),
    TYPED.job_id,
    uuid_generate_v4()
FROM
    airflow.answer_typed TYPED
    INNER JOIN airflow.survey_typed SUR ON SUR.source_id = TYPED.survey_id,
    jsonb_array_elements(TYPED.answers) ANS
WHERE TYPED.job_id = %(job_id)s :: BIGINT
    AND SUR.job_id = %(job_id)s :: BIGINT
;

ANALYZE airflow.answer_conform;

UPDATE airflow.answer_conform
SET
    question_id = 1
FROM
    airflow.answer_conform ac,
    airflow.question_typed qt,
    question q
WHERE
    qt.id = ac.question_id
