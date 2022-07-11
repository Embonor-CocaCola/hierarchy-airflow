SELECT s.id, ap.id, ap.origin_url, c.latitude, c.longitude, s.created_at, q.heading
FROM analyzed_photo ap
INNER JOIN survey s ON ap.survey_id = s.id
INNER JOIN customer c on s.customer_id = c.id
INNER JOIN question q on ap.question_id = q.id
WHERE ap.sent_ok = false
;
