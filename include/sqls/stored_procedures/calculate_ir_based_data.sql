CREATE OR REPLACE PROCEDURE calculate_ir_based_data()
    LANGUAGE SQL AS $$
        INSERT INTO preprocessed_ir (
                        is_pure,
                        co_cooler_co_products,
                        co_cooler_non_co_products,
                        stills_ss_water_unflavored_co,
                        stills_ms_water_unflavored_co,
                        stills_ss_water_unflavored_pe,
                        stills_ms_water_unflavored_pe,
                        stills_ss_water_flavored_co,
                        stills_ms_water_flavored_co,
                        stills_ss_water_flavored_pe,
                        stills_ms_water_flavored_pe,
                        stills_ss_ncbs_energy_co,
                        stills_ms_ncbs_energy_co,
                        stills_ss_ncbs_energy_pe,
                        stills_ms_ncbs_energy_pe,
                        stills_ss_ncbs_juice_co,
                        stills_ms_ncbs_juice_co,
                        stills_ss_ncbs_juice_pe,
                        stills_ms_ncbs_juice_pe,
                        stills_ss_ncbs_sports_co,
                        stills_ms_ncbs_sports_co,
                        stills_ss_ncbs_sports_pe,
                        stills_ms_ncbs_sports_pe,
                        ssd_ss_ret_co,
                        ssd_ss_ret_pe,
                        ssd_ss_ow_co,
                        ssd_ss_ow_pe,
                        ssd_ss_cola_co,
                        ssd_ss_cola_pe,
                        ssd_ss_flavor_co,
                        ssd_ss_flavor_pe,
                        ssd_ms_ret_co,
                        ssd_ms_ret_pe,
                        ssd_ms_ow_co,
                        ssd_ms_ow_pe,
                        ssd_ms_cola_co,
                        ssd_ms_cola_pe,
                        ssd_ms_flavor_co,
                        ssd_ms_flavor_pe,
                        survey_id
        )
        SELECT
            CASE count(*) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND p.recognition_details->>'is_foreign' = 'true')
            WHEN 0 THEN true ELSE false END
            is_pure,
            count(*) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND (p.recognition_details->>'is_foreign' != 'true' OR p.id = 54))
            co_cooler_co_products,
            count(*) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND (p.recognition_details->>'is_foreign' = 'true' OR p.id = 18))
            co_cooler_non_co_products,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' != 'SABORIZADA')
            stills_ss_water_unflavored_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' != 'SABORIZADA')
            stills_ms_water_unflavored_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' != 'SABORIZADA')
            stills_ss_water_unflavored_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' != 'SABORIZADA')
            stills_ms_water_unflavored_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' = 'SABORIZADA')
            stills_ss_water_flavored_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' = 'SABORIZADA')
            stills_ms_water_flavored_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' = 'SABORIZADA')
            stills_ss_water_flavored_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'AGUA' AND p.details->>'local_category_name' = 'SABORIZADA')
            stills_ms_water_flavored_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'ENERGIZANTES')
            stills_ss_ncbs_energy_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'ENERGIZANTES')
            stills_ms_ncbs_energy_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'ENERGIZANTES')
            stills_ss_ncbs_energy_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'ENERGIZANTES')
            stills_ms_ncbs_energy_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' IN ('JUGOS','KAPO','LACTEOS'))
            stills_ss_ncbs_juice_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' IN ('JUGOS','KAPO','LACTEOS'))
            stills_ms_ncbs_juice_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' IN ('JUGOS','KAPO','LACTEOS'))
            stills_ss_ncbs_juice_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' IN ('JUGOS','KAPO','LACTEOS'))
            stills_ms_ncbs_juice_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'SPORT DRINK')
            stills_ss_ncbs_sports_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'SPORT DRINK')
            stills_ms_ncbs_sports_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'SS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'SPORT DRINK')
            stills_ss_ncbs_sports_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'group' like 'MS%' AND p.details->>'category' = 'NCB' AND p.details->>'local_category_name' = 'SPORT DRINK')
            stills_ms_ncbs_sports_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'SS RET')
            ssd_ss_ret_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'SS RET')
            ssd_ss_ret_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'SS OW')
            ssd_ss_ow_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'SS OW')
            ssd_ss_ow_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'SS%' AND p.details->>'flavour_name' = 'Cola')
            ssd_ss_cola_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'SS%' AND p.details->>'flavour_name' = 'Cola')
            ssd_ss_cola_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'SS%' AND p.details->>'flavour_name' != 'Cola')
            ssd_ss_flavor_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'SS%' AND p.details->>'flavour_name' != 'Cola')
            ssd_ss_flavor_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'MS RET')
            ssd_ms_ret_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'MS RET')
            ssd_ms_ret_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'MS OW')
            ssd_ms_ow_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' = 'MS OW')
            ssd_ms_ow_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'MS%' AND p.details->>'flavour_name' = 'Cola')
            ssd_ms_cola_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'MS%' AND p.details->>'flavour_name' = 'Cola')
            ssd_ms_cola_pe,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'MS%' AND p.details->>'flavour_name' != 'Cola')
            ssd_ms_flavor_co,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' = 'true' AND p.details->>'category' = 'SSD' AND p.details->>'group' like 'MS%' AND p.details->>'flavour_name' != 'Cola')
            ssd_ms_flavor_pe,
            s.id
        FROM survey s
            INNER JOIN analyzed_photo ap on s.id = ap.survey_id
            INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
            INNER JOIN product p on rp.product_id = p.id
        WHERE s.skips_survey = false
        GROUP BY s.id
        ON CONFLICT (survey_id) DO UPDATE SET
            is_pure = excluded.is_pure,
            co_cooler_co_products = excluded.co_cooler_co_products,
            co_cooler_non_co_products = excluded.co_cooler_non_co_products,
            stills_ss_water_unflavored_co = excluded.stills_ss_water_unflavored_co,
            stills_ms_water_unflavored_co = excluded.stills_ms_water_unflavored_co,
            stills_ss_water_unflavored_pe = excluded.stills_ss_water_unflavored_pe,
            stills_ms_water_unflavored_pe = excluded.stills_ms_water_unflavored_pe,
            stills_ss_water_flavored_co = excluded.stills_ss_water_flavored_co,
            stills_ms_water_flavored_co = excluded.stills_ms_water_flavored_co,
            stills_ss_water_flavored_pe = excluded.stills_ss_water_flavored_pe,
            stills_ms_water_flavored_pe = excluded.stills_ms_water_flavored_pe,
            stills_ss_ncbs_energy_co = excluded.stills_ss_ncbs_energy_co,
            stills_ms_ncbs_energy_co = excluded.stills_ms_ncbs_energy_co,
            stills_ss_ncbs_energy_pe = excluded.stills_ss_ncbs_energy_pe,
            stills_ms_ncbs_energy_pe = excluded.stills_ms_ncbs_energy_pe,
            stills_ss_ncbs_juice_co = excluded.stills_ss_ncbs_juice_co,
            stills_ms_ncbs_juice_co = excluded.stills_ms_ncbs_juice_co,
            stills_ss_ncbs_juice_pe = excluded.stills_ss_ncbs_juice_pe,
            stills_ms_ncbs_juice_pe = excluded.stills_ms_ncbs_juice_pe,
            stills_ss_ncbs_sports_co = excluded.stills_ss_ncbs_sports_co,
            stills_ms_ncbs_sports_co = excluded.stills_ms_ncbs_sports_co,
            stills_ss_ncbs_sports_pe = excluded.stills_ss_ncbs_sports_pe,
            stills_ms_ncbs_sports_pe = excluded.stills_ms_ncbs_sports_pe,
            ssd_ss_ret_co = excluded.ssd_ss_ret_co,
            ssd_ss_ret_pe = excluded.ssd_ss_ret_pe,
            ssd_ss_ow_co = excluded.ssd_ss_ow_co,
            ssd_ss_ow_pe = excluded.ssd_ss_ow_pe,
            ssd_ss_cola_co = excluded.ssd_ss_cola_co,
            ssd_ss_cola_pe = excluded.ssd_ss_cola_pe,
            ssd_ss_flavor_co = excluded.ssd_ss_flavor_co,
            ssd_ss_flavor_pe = excluded.ssd_ss_flavor_pe,
            ssd_ms_ret_co = excluded.ssd_ms_ret_co,
            ssd_ms_ret_pe = excluded.ssd_ms_ret_pe,
            ssd_ms_ow_co = excluded.ssd_ms_ow_co,
            ssd_ms_ow_pe = excluded.ssd_ms_ow_pe,
            ssd_ms_cola_co = excluded.ssd_ms_cola_co,
            ssd_ms_cola_pe = excluded.ssd_ms_cola_pe,
            ssd_ms_flavor_co = excluded.ssd_ms_flavor_co,
            ssd_ms_flavor_pe = excluded.ssd_ms_flavor_pe
            ;
$$;
