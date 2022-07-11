UPDATE survey
SET reset_at = now()
WHERE id = ANY(%(survey_source_ids)s);
