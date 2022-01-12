SELECT a.self_evaluation_id, json_agg(json_build_object(
        'question', q.*,
        'attachments', a.attachments
    )) FROM answer a INNER JOIN question q on a.question_id = q.id
WHERE a.question_id IN %(q_id)s
    AND a.self_evaluation_id IN %(ev_id)s
    AND cardinality(a.attachments) > 0
GROUP BY a.self_evaluation_id
;
