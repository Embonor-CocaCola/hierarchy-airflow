SELECT
    json_build_object('surveyId', s.source_id, 'vendorId', v.source_id::text, 'customerId', c.source_id::text)
FROM survey s
INNER JOIN vendor v on v.id = s.vendor_id
INNER JOIN customer c on c.id = s.customer_id
INNER JOIN evaluation_status es on s.evaluation_status_id = es.id
WHERE s.created_at between now() - interval '23 days' and now()
    AND s.reset_at IS NULL;
