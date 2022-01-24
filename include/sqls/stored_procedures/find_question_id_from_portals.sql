CREATE OR REPLACE FUNCTION find_question_id_from_portals(in_array jsonb, id_to_find varchar, current_job_id integer)
            RETURNS varchar AS $$
            DECLARE
                portals jsonb := in_array;
                portal jsonb;

                pages jsonb;
                page jsonb;

                questions jsonb;
                question jsonb;

                found_id varchar;
            BEGIN
                FOR portal IN SELECT * FROM jsonb_array_elements(portals)
                LOOP

                    pages := portal->'pages';
                    FOR page IN SELECT * FROM jsonb_array_elements(pages)
                    LOOP
                        questions := page->'questions';
                        FOR question IN SELECT * FROM jsonb_array_elements(questions)
                        LOOP
                           IF question->>'id' = id_to_find THEN
                                found_id := question->'question'->>'$oid';
                                SELECT id INTO found_id FROM airflow.question_typed WHERE source_id = found_id
                                    AND job_id = current_job_id;
                                RETURN found_id;
                            END IF;
                        END LOOP;

                    END LOOP;

                END LOOP;
                RAISE EXCEPTION 'Requested question_id not found: %s', id_to_find;
            END;
                $$ LANGUAGE plpgsql;
