CREATE OR REPLACE PROCEDURE calculate_ir_based_data()
    LANGUAGE SQL AS $$
        INSERT INTO preprocessed_ir (
                        is_pure,
                        total_cooler_products,
                        embonor_products,
                        ssd_amount,
                        stills_amount,
                        returnable_amount,
                        disposable_amount,
                        waters_amount,
                        ncbs_amount,
                        survey_id
        )
        SELECT
            CASE count(*) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND p.recognition_details->>'is_foreign' = 'true')
            WHEN 0 THEN true ELSE false END
            is_pure,
            count(*) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1')
            total_cooler_products,
            count(*) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND p.recognition_details->>'is_foreign' != 'true')
            embonor_products,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD')
            ssd_amount,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' IN ('AGUA', 'NCB', 'OTROS'))
            stills_amount,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.display->>'package_type' IN ('TP', 'PET', 'VNR', 'LATA', 'SAC', 'TBD') )
            returnable_amount,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'SSD' AND p.display->>'package_type' IN ('RP', 'V.RET', 'RGB') )
            disposable_amount,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'AGUA')
            waters_amount,
            count(*) FILTER ( WHERE p.recognition_details->>'is_foreign' != 'true' AND p.details->>'category' = 'NCB')
            ncbs_amount,
            s.id
        FROM survey s
            INNER JOIN analyzed_photo ap on s.id = ap.survey_id
            INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
            INNER JOIN product p on rp.product_id = p.id
        WHERE s.skips_survey = false
        GROUP BY s.id
        ON CONFLICT (survey_id) DO UPDATE SET
            is_pure = excluded.is_pure,
            total_cooler_products = excluded.total_cooler_products,
            embonor_products = excluded.embonor_products,
            ssd_amount = excluded.ssd_amount,
            stills_amount = excluded.stills_amount,
            returnable_amount = excluded.returnable_amount,
            disposable_amount = excluded.disposable_amount,
            waters_amount = excluded.waters_amount,
            ncbs_amount = excluded.ncbs_amount,
            essentials_compliant = excluded.essentials_compliant,
            success_photo_compliant = excluded.success_photo_compliant
;
$$;
