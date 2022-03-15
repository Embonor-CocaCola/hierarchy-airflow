UPDATE public.survey_analysis sa
SET status = 'ready'
WHERE survey_id = %(survey_id)s;
