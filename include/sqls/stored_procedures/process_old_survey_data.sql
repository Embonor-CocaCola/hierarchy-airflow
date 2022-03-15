CREATE OR REPLACE PROCEDURE process_old_survey_data()
    LANGUAGE plpgsql
    AS $$
    DECLARE
        qn record;
        old_source varchar;
        new_id uuid;
    BEGIN
        CREATE TABLE tmp_question_counterparts(
            source_id varchar,
            target_id uuid
        );

        FOR qn IN SELECT * FROM question
        LOOP
            old_source := qn.source_id;

            CASE qn.heading
                WHEN '¿Tenemos el 60% del espacio en SSD? Se sugiere agregar dos imágenes.'
                    THEN
                        SELECT id INTO new_id from question
                        where heading
                        LIKE 'Considerando el total de la categoría SSD, ¿Tenemos el 60%';
                WHEN '¿Tenemos el 40% del espacio en STILLS? Se sugiere agregar dos imágenes.'
                    THEN
                        SELECT id INTO new_id from question
                        where heading
                        LIKE 'Considerando el total de la categoría Stills, ¿Tenemos el 40%';
                WHEN '¿Están los equipos de frío Coca-Cola Embonor puros?'
                    THEN
                        SELECT id INTO new_id from question
                        WHERE heading
                        LIKE '¿Están los equipos de frío Embonor puros?';
                WHEN '¿Estan los%Equipos de Frío llenos al menos en un 75%?'
                    THEN
                        SELECT id INTO new_id from question
                        WHERE heading
                        LIKE '¿Estan los equipos de frío Embonor llenos al menos en un 75%';
                ELSE
                    CONTINUE;
            END CASE;

            INSERT INTO tmp_question_counterparts(source_id, target_id) VALUES (old_source, new_id);
        END LOOP;

    UPDATE answer
        SET question_id = tmp.target_id
        FROM
            answer TARGET,
            tmp_question_counterparts tmp,
            question q
        WHERE TARGET.question_id = q.id
            AND q.source_id = tmp.source_id;

    DROP TABLE tmp_question_counterparts;
    END;
    $$
