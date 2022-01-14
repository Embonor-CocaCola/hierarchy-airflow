INSERT INTO analyzed_photo (
    id,
    scene_type,
    sub_scene_type,
    self_evaluation_id,
    self_evaluation_analysis_id,
    question_id,
    origin_url,
    sent_ok
)
VALUES (
    %(scene_id)s,
    %(scene_type)s,
    %(sub_scene_type)s,
    %(survey_id)s,
    %(analysis_id)s,
    %(question_id)s,
    %(origin_url)s,
    %(sent_ok)s
)
;
