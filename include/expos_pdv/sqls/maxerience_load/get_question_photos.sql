SELECT a.survey_id, json_agg(json_build_object(
        'question', q.*,
        'attachments', a.attachments
        )),
        c.latitude,
        c.longitude,
        s.created_at :: TEXT
FROM answer a
INNER JOIN question q on a.question_id = q.id
INNER JOIN survey s on a.survey_id = s.id
INNER JOIN customer c on s.customer_id = c.id
LEFT JOIN analyzed_photo ap on ap.survey_id = a.survey_id AND ap.question_id = a.question_id
WHERE a.question_id IN %(q_id)s
    AND a.survey_id IN %(ev_id)s
    AND cardinality(a.attachments) > 0
    AND ap.sent_ok IS NULL
GROUP BY
    a.survey_id,
    c.latitude,
    c.longitude,
    s.created_at
;
