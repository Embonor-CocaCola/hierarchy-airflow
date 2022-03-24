DROP FUNCTION IF EXISTS remove_rut_leading_zero(rut text);
CREATE OR REPLACE FUNCTION remove_rut_leading_zero(rut text)
    RETURNS text
    AS $$
    BEGIN
        IF substring(rut,1,1) = '0'
        THEN
            RETURN substring(rut,2);
        END IF;

        RETURN rut;
    END;
$$ LANGUAGE plpgsql;
