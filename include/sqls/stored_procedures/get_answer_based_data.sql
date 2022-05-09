-- WARNING: Be careful when updating this function because it is called to populate two materialized
-- views for Expos-Service. If you change a column name, be sure to also change it in the code!
CREATE OR REPLACE FUNCTION get_answer_based_data()
    RETURNS TABLE
            (
                is_first_position        boolean,
                is_pure                  boolean,
                tagged_price             boolean,
                has_sixty_percent_ssd    boolean,
                has_forty_percent_stills boolean,
                has_edf                  boolean,
                filled_75_percent        boolean,
                has_outside_banners      boolean,
                survey_id                uuid
            )
AS
$$
BEGIN
    RETURN QUERY SELECT CASE
               WHEN count(*) FILTER ( WHERE q.heading ilike '%Se encuentra% Embonor en primera posición?%' and
                                            a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*) FILTER ( WHERE q.heading ilike '%Se encuentra% Embonor en primera posición?%' and
                                            a.values ->> 0 = 'false') = 1
                   THEN false
               END
               is_first_position,
           CASE
               WHEN count(*) FILTER ( WHERE q.heading = '¿Están los equipos de frío Embonor puros?' and
                                            a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*) FILTER ( WHERE q.heading = '¿Están los equipos de frío Embonor puros?' and
                                            a.values ->> 0 = 'false') = 1
                   THEN false
               END
               is_pure,
           CASE
               WHEN count(*)
                    FILTER ( WHERE q.heading = '¿Se encuentran marcados los precios?' and a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*)
                    FILTER ( WHERE q.heading = '¿Se encuentran marcados los precios?' and a.values ->> 0 = 'false') = 1
                   THEN false
               END
               tagged_price,
           CASE
               WHEN count(*) FILTER ( WHERE q.heading =
                                            'Considerando el total de la categoría SSD, ¿Tenemos el 60% del espacio en relación a la competencia? (Considerar frío + ambiente)' and
                                            a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*) FILTER ( WHERE q.heading =
                                            'Considerando el total de la categoría SSD, ¿Tenemos el 60% del espacio en relación a la competencia? (Considerar frío + ambiente)' and
                                            a.values ->> 0 = 'false') = 1
                   THEN false
               END
               has_sixty_percent_ssd,
           CASE
               WHEN count(*) FILTER ( WHERE q.heading =
                                            'Considerando el total de la categoría Stills, ¿Tenemos el 40% del espacio en relación a la competencia? (Considerar frío + ambiente)' and
                                            a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*) FILTER ( WHERE q.heading =
                                            'Considerando el total de la categoría Stills, ¿Tenemos el 40% del espacio en relación a la competencia? (Considerar frío + ambiente)' and
                                            a.values ->> 0 = 'false') = 1
                   THEN false
               END
               has_forty_percent_stills,
           CASE
               WHEN count(*) FILTER ( WHERE q.heading = '¿El cliente tiene uno o más equipos de frío Embonor?' and
                                            a.values ->> 0 = 'Si') = 1 -- Notice that this answer is not boolean
                   THEN true
               ELSE false
               END
               has_edf,
           CASE
               WHEN count(*)
                    FILTER ( WHERE q.heading = '¿Estan los equipos de frío Embonor llenos al menos en un 75%?' and
                                   a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*)
                    FILTER ( WHERE q.heading = '¿Estan los equipos de frío Embonor llenos al menos en un 75%?' and
                                   a.values ->> 0 = 'false') = 1
                   THEN false
               END
               filled_75_percent,
           CASE
               WHEN count(*) FILTER ( WHERE q.heading =
                                            '¿Están el Cuatripendón y el Afiche Single Serve implementados en el exterior del punto de venta? Si/No, Incluir una foto' and
                                            a.values ->> 0 = 'true') = 1
                   THEN true
               WHEN count(*) FILTER ( WHERE q.heading =
                                            '¿Están el Cuatripendón y el Afiche Single Serve implementados en el exterior del punto de venta? Si/No, Incluir una foto' and
                                            a.values ->> 0 = 'false') = 1
                   THEN false
               END
               has_outside_banners,
           s.id
    FROM survey s
             INNER JOIN answer a on s.id = a.survey_id
             INNER JOIN question q on q.id = a.question_id
    WHERE s.skips_survey = false
    GROUP BY s.id;
END;
$$ LANGUAGE plpgsql;
