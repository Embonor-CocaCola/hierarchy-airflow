UPDATE public.survey_analysis sa
SET
status = 'ready',
updated_at = now()
WHERE survey_id = %(survey_id)s;
