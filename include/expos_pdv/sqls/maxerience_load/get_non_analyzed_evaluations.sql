SELECT se.id FROM survey se
    LEFT JOIN survey_analysis sea on se.id = sea.survey_id
    WHERE sea.id IS NULL;
