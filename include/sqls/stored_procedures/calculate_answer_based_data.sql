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
            has_outside_banners,
            survey_id
        )
        SELECT
            CASE
                WHEN count(*) FILTER ( WHERE q.heading ilike '%Se encuentra% Embonor en primera posición?%' and a.values->>0 = 'true') = 1
            THEN true
                WHEN count(*) FILTER ( WHERE q.heading ilike '%Se encuentra% Embonor en primera posición?%' and a.values->>0 = 'false') = 1
            THEN false
            END
            is_first_position,
            CASE
                WHEN count(*) FILTER ( WHERE q.heading = '¿Están los equipos de frío Embonor puros?' and a.values->>0 = 'true') = 1
            THEN true
                WHEN count(*) FILTER ( WHERE q.heading = '¿Están los equipos de frío Embonor puros?' and a.values->>0 = 'false') = 1
            THEN false
            END
            is_pure,
            CASE WHEN count(*) FILTER ( WHERE q.heading = '¿Se encuentran marcados los precios?' and a.values->>0 = 'true') = 1
            THEN true
            WHEN count(*) FILTER ( WHERE q.heading = '¿Se encuentran marcados los precios?' and a.values->>0 = 'false') = 1
            THEN false
            END
            tagged_price,
            CASE WHEN count(*) FILTER ( WHERE q.heading = 'Considerando el total de la categoría SSD, ¿Tenemos el 60% del espacio en relación a la competencia? (Considerar frío + ambiente)' and a.values->>0 = 'true') = 1
            THEN true
            WHEN count(*) FILTER ( WHERE q.heading = 'Considerando el total de la categoría SSD, ¿Tenemos el 60% del espacio en relación a la competencia? (Considerar frío + ambiente)' and a.values->>0 = 'false') = 1
            THEN false
            END
            has_sixty_percent_ssd,
            CASE WHEN count(*) FILTER ( WHERE q.heading = 'Considerando el total de la categoría Stills, ¿Tenemos el 40% del espacio en relación a la competencia? (Considerar frío + ambiente)' and a.values->>0 = 'true') = 1
            THEN true
            WHEN count(*) FILTER ( WHERE q.heading = 'Considerando el total de la categoría Stills, ¿Tenemos el 40% del espacio en relación a la competencia? (Considerar frío + ambiente)' and a.values->>0 = 'false') = 1
            THEN false
            END
            has_forty_percent_stills,
            CASE WHEN count(*) FILTER ( WHERE q.heading = '¿El cliente tiene uno o más equipos de frío Embonor?' and a.values->>0 = 'Si') = 1 -- Notice that this answer is not boolean
            THEN true
            ELSE false
            END
            has_edf,
            CASE WHEN count(*) FILTER ( WHERE q.heading = '¿Estan los equipos de frío Embonor llenos al menos en un 75%?' and a.values->>0 = 'true') = 1
            THEN true
            WHEN count(*) FILTER ( WHERE q.heading = '¿Estan los equipos de frío Embonor llenos al menos en un 75%?' and a.values->>0 = 'false') = 1
            THEN false
            END
            filled_75_percent,
            CASE WHEN count(*) FILTER ( WHERE q.heading = '¿Están el Cuatripendón y el Afiche Single Serve implementados en el exterior del punto de venta? Si/No, Incluir una foto' and a.values->>0 = 'true') = 1
            THEN true
            WHEN count(*) FILTER ( WHERE q.heading = '¿Están el Cuatripendón y el Afiche Single Serve implementados en el exterior del punto de venta? Si/No, Incluir una foto' and a.values->>0 = 'false') = 1
            THEN false
            END
            has_outside_banners,
            s.id
        FROM survey s
            INNER JOIN answer a on s.id = a.survey_id
            INNER JOIN question q on q.id = a.question_id
        WHERE s.skips_survey = false
        GROUP BY s.id
        ON CONFLICT (survey_id) DO UPDATE SET
        is_first_position = excluded.is_first_position,
        is_pure = excluded.is_pure,
        tagged_price = excluded.tagged_price,
        has_sixty_percent_ssd = excluded.has_sixty_percent_ssd,
        has_forty_percent_stills = excluded.has_forty_percent_stills,
        has_edf = excluded.has_edf,
        filled_75_percent = excluded.filled_75_percent,
        has_outside_banners = excluded.has_outside_banners
;
$$;
