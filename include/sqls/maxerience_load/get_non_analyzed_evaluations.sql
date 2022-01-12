SELECT se.id FROM self_evaluation se
    LEFT JOIN self_evaluation_analysis sea on se.self_evaluation_analysis_id = sea.id
    WHERE se.self_evaluation_analysis_id IS NULL;
