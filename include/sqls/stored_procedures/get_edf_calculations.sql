-- WARNING: Be careful when updating this function because it is called to populate two materialized
-- views for Expos-Service. If you change a column name, be sure to also change it in the code!
CREATE OR REPLACE FUNCTION get_edf_calculations()
    RETURNS TABLE
            (
                is_pure                   boolean,
                co_cooler_co_products     smallint,
                co_cooler_non_co_products smallint,
                survey_id                 uuid
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT CASE count(rp.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                                        p.is_foreign is true)::smallint
                   WHEN 0::smallint THEN true
                   ELSE false END
                    is_pure,
               count(rp.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                                   (p.is_foreign is not true OR p.id = 54))::smallint
                    co_cooler_co_products,
               count(rp.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                                   (p.is_foreign is true OR p.id = 18))::smallint
                    co_cooler_non_co_products,
               s.id survey_id
        FROM survey s
                 INNER JOIN analyzed_photo ap on s.id = ap.survey_id
                 INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
                 INNER JOIN product p on rp.product_id = p.id
        GROUP BY s.id;
END;
$$
    LANGUAGE 'plpgsql';
