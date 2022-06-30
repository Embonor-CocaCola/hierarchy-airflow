CREATE OR REPLACE FUNCTION clean_survey_collection_ids(in_array jsonb)
            RETURNS jsonb AS $$
            DECLARE
                portals jsonb := in_array;
                portal jsonb;
                new_portals jsonb;
                portal_as_str text;

                pages jsonb;
                page jsonb;
                new_pages jsonb;

                questions jsonb;
                question jsonb;
                new_questions jsonb;
            BEGIN
                new_portals := jsonb_build_array();
                FOR portal IN SELECT * FROM jsonb_array_elements(portals)
                LOOP
                    new_pages := jsonb_build_array();

                    portal_as_str := portal :: text;
                    portal_as_str := replace(portal_as_str, '_id', 'id');
                    portal := portal_as_str :: jsonb;
                    pages := portal->'pages';
                    FOR page IN SELECT * FROM jsonb_array_elements(pages)
                    LOOP
                        new_questions := jsonb_build_array();
                        questions := page->'questions';
                        FOR question IN SELECT * FROM jsonb_array_elements(questions)
                        LOOP
                            new_questions := new_questions || (question || jsonb_build_object(
                                'id', stringify_oid(question->>'id'),
                                'question', stringify_oid(question->>'question')
                            ));
                        END LOOP;
                        new_pages := new_pages || (page || jsonb_build_object(
                            'id', stringify_oid(page->>'id'),
                            'questions', new_questions
                        ));
                    END LOOP;
                    new_portals := new_portals || (portal || jsonb_build_object(
                        'id', stringify_oid(portal->>'id'),
                        'pages', new_pages
                    ));
                END LOOP;
                RETURN new_portals;
            END;
            $$ LANGUAGE plpgsql;
