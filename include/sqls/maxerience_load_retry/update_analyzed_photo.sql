UPDATE analyzed_photo
SET sent_ok = %(sent_ok)s
WHERE id = %(scene_id)s :: uuid;
