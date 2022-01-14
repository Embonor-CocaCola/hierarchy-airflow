SELECT se.id FROM self_evaluation se
    LEFT JOIN self_evaluation_analysis sea on se.id = sea.self_evaluation_id
    WHERE sea.id IS NULL;
