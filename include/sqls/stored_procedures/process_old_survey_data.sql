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
            RAISE NOTICE 'Inserting entry in tmp table for question %', qn.heading;
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
                WHEN '¿Estan los  Equipos de Frío llenos al menos en un 75%?'
                    THEN
                        SELECT id INTO new_id from question
                        WHERE heading
                        LIKE '¿Estan los equipos de frío Embonor llenos al menos en un 75%';
                WHEN '¿Se encuentra el equipo de frío en primera posición?'
                    THEN
                        SELECT id INTO new_id from question
                        WHERE heading
                        LIKE '¿Se encuentra el equipo de frío Embonor en primera posición?';
                ELSE
                    CONTINUE;
            END CASE;

            RAISE NOTICE 'new id = %', new_id;
            INSERT INTO tmp_question_counterparts(source_id, target_id) VALUES (old_source, new_id);
            RAISE NOTICE 'Entry inserted in tmp_question_counterparts table';
            ANALYZE tmp_question_counterparts;
        END LOOP;

    RAISE NOTICE 'Looping and building of tmp table completed. Attempting to update answers';
    UPDATE answer TARGET
        SET question_id = tmp.target_id
        FROM
            tmp_question_counterparts tmp,
            question q
        WHERE TARGET.question_id = q.id
            AND q.source_id = tmp.source_id;

    RAISE NOTICE 'updated answers successfully';
    DROP TABLE tmp_question_counterparts;
    RAISE NOTICE 'tmp table dropped';
    END;
    $$;
