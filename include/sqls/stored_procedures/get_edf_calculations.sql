-- WARNING: Be careful when updating this function because it is called to populate two materialized
-- views for Expos-Service. If you change a column name, be sure to also change it in the code!
    BEGIN;
    DROP MATERIALIZED VIEW IF EXISTS public.preprocessed_edf CASCADE;

    DROP FUNCTION IF EXISTS get_edf_calculations();

    CREATE OR REPLACE FUNCTION get_edf_calculations()
        RETURNS TABLE
                (
                    is_pure                    boolean,
                    co_cooler_co_products      smallint,
                    co_cooler_non_co_products  smallint,
                    co_cooler_empty_products   smallint,
                    pe_cooler_empty_products   smallint,
                    co_cooler_foreign_products smallint,
                    pe_cooler_foreign_products smallint,
                    co_cooler_total_products   smallint,
                    pe_cooler_total_products   smallint,
                    survey_id                  uuid
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
                                               (p.is_foreign is false OR p.id = 54))::smallint
                        co_cooler_co_products,
                   count(rp.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                               (p.is_foreign is true OR p.id = 18))::smallint
                        co_cooler_non_co_products,
                   count(rp.id)
                   FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' and rp.product_id = 18) :: smallint
                        co_cooler_empty_products,
                   count(rp.id)
                   FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '2' and rp.product_id = 18) :: smallint
                        pe_cooler_empty_products,
                   count(rp.id)
                   FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' and rp.product_id = 54) :: smallint
                        co_cooler_foreign_products,
                   count(rp.id)
                   FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '2' and rp.product_id = 54) :: smallint
                        pe_cooler_foreign_products,
                   count(rp.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' ) :: smallint
                        co_cooler_total_products,
                   count(rp.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '2' ) :: smallint
                        pe_cooler_total_products,
                   s.id survey_id
            FROM survey s
                     INNER JOIN analyzed_photo ap on s.id = ap.survey_id
                     INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
                     INNER JOIN product p on rp.product_id = p.id
            GROUP BY s.id;
    END;
    $$
        LANGUAGE 'plpgsql';

    CREATE MATERIALIZED VIEW public."preprocessed_edf" AS
    select *
    from get_edf_calculations();
    CREATE UNIQUE INDEX uidx_preprocessed_edf_survey_id ON public.preprocessed_edf (survey_id);
    COMMIT;
