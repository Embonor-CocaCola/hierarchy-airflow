CREATE OR REPLACE FUNCTION stringify_oid(oid_or_string text)
            RETURNS text AS $$
            DECLARE

            BEGIN
                IF oid_or_string like '{"$oid%' then
                    return oid_or_string::json->>'$oid';
                else
                    return oid_or_string;
                end if;
            END;
                $$ LANGUAGE plpgsql immutable;

CREATE OR REPLACE FUNCTION stringify_oid(oid_or_string json)
            RETURNS text AS $$
            DECLARE

            BEGIN
                return oid_or_string::json->>'$oid';
            END;
                $$ LANGUAGE plpgsql immutable;

CREATE OR REPLACE FUNCTION stringify_oid(oid_or_string jsonb)
            RETURNS text AS $$
            DECLARE

            BEGIN
                return oid_or_string::json->>'$oid';
            END;
                $$ LANGUAGE plpgsql immutable;
