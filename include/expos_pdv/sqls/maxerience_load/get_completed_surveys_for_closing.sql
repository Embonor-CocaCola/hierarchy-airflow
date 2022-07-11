SELECT *, floor(extract(epoch from now()) * 1000) as session_end_at FROM
(
SELECT
    (COUNT(ap.id) FILTER( WHERE ap.sent_ok = true AND ap.parquet_file_id is null ) = COUNT(ap.id)) AS ready_for_closing,
    COUNT(ap.id) AS total_images,
    sa.survey_id,
    floor(extract(epoch from sa.created_at) * 1000) as session_start_at,
    s.created_at :: date :: text as visit_date
FROM public.survey_analysis sa
INNER JOIN analyzed_photo ap on sa.survey_id = ap.survey_id
INNER JOIN survey s on ap.survey_id = s.id
WHERE sa.status = 'in_progress'
GROUP BY sa.survey_id, session_start_at, visit_date) subquery
WHERE ready_for_closing = true;
