SELECT a.survey_id, json_agg(json_build_object(
        'question', q.*,
        'attachments', a.attachments
        )),
        c.latitude,
        c.longitude,
        se.created_at :: TEXT
FROM answer a
INNER JOIN question q on a.question_id = q.id
INNER JOIN survey se on a.survey_id = se.id
INNER JOIN customer c on se.customer_id = c.id
WHERE a.question_id IN %(q_id)s
    AND a.survey_id IN %(ev_id)s
    AND cardinality(a.attachments) > 0
GROUP BY
    a.survey_id,
    c.latitude,
    c.longitude,
    se.created_at
;
