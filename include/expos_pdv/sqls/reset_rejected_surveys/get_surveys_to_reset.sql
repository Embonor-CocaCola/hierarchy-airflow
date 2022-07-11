SELECT
    array_agg(json_build_object('surveyId', s.source_survey_id, 'vendorId', v.source_id::text, 'customerId', c.source_id::text)) payload,
    array_agg(s.id::text)::text[] survey_ids
FROM survey s
INNER JOIN vendor v on v.id = s.vendor_id
INNER JOIN customer c on c.id = s.customer_id
INNER JOIN evaluation_status es on s.evaluation_status_id = es.id
WHERE s.created_at between now() - interval '1 day' and now()
    AND es.code = 'R'
    AND s.reset_at IS NULL;
