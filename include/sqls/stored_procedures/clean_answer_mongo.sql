CREATE OR REPLACE FUNCTION clean_answer_collection_ids(in_array jsonb)
            RETURNS jsonb AS $$
            DECLARE
                arr jsonb := in_array;
                elem jsonb;
                elem_as_str text;
                new_arr jsonb := jsonb_build_array();
            BEGIN
                FOR elem IN SELECT * FROM jsonb_array_elements(arr)
                LOOP
                    elem_as_str := elem :: text;
                    elem_as_str := replace(elem_as_str, '_id', 'id');
                    elem := elem_as_str :: jsonb;
                    new_arr := new_arr || (elem || jsonb_build_object('questionId', elem->'questionId'->>'$oid', 'id', elem->'id'->>'$oid'));
                END LOOP;
                RETURN new_arr;
            END;
            $$ LANGUAGE plpgsql;
