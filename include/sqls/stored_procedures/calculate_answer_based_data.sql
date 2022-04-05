CREATE OR REPLACE PROCEDURE calculate_answer_based_data()
    LANGUAGE SQL AS $$
        INSERT INTO preprocessed_answer (
            is_first_position,
            is_pure,
            tagged_price,
            has_sixty_percent_ssd,
            has_forty_percent_stills,
            has_edf,
            filled_75_percent,
            survey_id
        )
        SELECT
            CASE count(*) FILTER ( WHERE q.heading = '¿Se encuentra el equipo de frío Embonor en primera posición?' and a.values->>0 = 'true')
            WHEN 1 THEN true ELSE false END
            is_first_position,
            CASE count(*) FILTER ( WHERE q.heading = '¿Están los equipos de frío Embonor puros?' and a.values->>0 = 'true')
            WHEN 1 THEN true ELSE false END
            is_pure_by_answer,
            CASE count(*) FILTER ( WHERE q.heading = '¿Se encuentran marcados los precios?' and a.values->>0 = 'true')
            WHEN 1 THEN true ELSE false END
            tagged_price,
            CASE count(*) FILTER ( WHERE q.heading = 'Considerando el total de la categoría SSD, ¿Tenemos el 60% del espacio en relación a la competencia? (Considerar frío + ambiente)' and a.values->>0 = 'true')
            WHEN 1 THEN true ELSE false END
            has_sixty_percent_ssd,
            CASE count(*) FILTER ( WHERE q.heading = 'Considerando el total de la categoría Stills, ¿Tenemos el 40% del espacio en relación a la competencia? (Considerar frío + ambiente)' and a.values->>0 = 'true')
            WHEN 1 THEN true ELSE false END
            has_forty_percent_stills,
            CASE count(*) FILTER ( WHERE q.heading = '¿El cliente tiene uno o más equipos de frío Embonor?' and a.values->>0 = 'Si') -- Notice that this answer is not boolean
            WHEN 1 THEN true ELSE false END
            has_edf,
            CASE count(*) FILTER ( WHERE q.heading = '¿Estan los equipos de frío Embonor llenos al menos en un 75%?' and a.values->>0 = 'true')
            WHEN 1 THEN true ELSE false END
            filled_75_percent,
            s.id
        FROM survey s
            INNER JOIN answer a on s.id = a.survey_id
            INNER JOIN question q on q.id = a.question_id
        WHERE s.skips_survey = false
        GROUP BY s.id
        ON CONFLICT (survey_id) DO NOTHING;
$$;
