UPDATE survey
SET reset_at = now()
WHERE source_id = ANY(%(survey_source_ids)s);
