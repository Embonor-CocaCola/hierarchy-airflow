CREATE OR REPLACE PROCEDURE calculate_ir_based_data()
    LANGUAGE SQL AS
$$
with recursive
    compliance as (
        SELECT CASE
                   WHEN spp.flavors > 1
                       THEN
                       LEAST(LEAST(count(distinct rp.product_id) filter (
                           where p.sku = ANY (spp.skus)
                           ), spp.flavors) * (spp.required_facings / spp.flavors), count(rp.id) filter (
                           where p.sku = ANY (spp.skus)
                           ))
                   ELSE
                       LEAST(count(rp.id) filter (
                           where p.sku = ANY (spp.skus)
                           ), spp.required_facings)
                   END present_facings,
               spp.required_facings,
               spp.is_essential,
               s.id    survey_id
        FROM survey s
                 INNER JOIN analyzed_photo ap on s.id = ap.survey_id
                 INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
                 INNER JOIN product p on rp.product_id = p.id
                 INNER JOIN customer c on s.customer_id = c.id
                 INNER JOIN success_photo_product spp on spp.cluster_id = c.cluster_id
        WHERE s.skips_survey IS NOT TRUE
        GROUP BY s.id, spp.id
    ),
    aggregated_compliance AS (
        select sum(compliance.present_facings) filter ( where is_essential is true )  essential_facings,
               sum(compliance.required_facings) filter ( where is_essential is true ) required_essential_facings,
               sum(compliance.present_facings)                                        success_photo_facings,
               sum(compliance.required_facings)                                       required_success_photo_facings,
               compliance.survey_id
        from compliance
        group by compliance.survey_id
    ),
    product_sums AS (
        SELECT CASE count(distinct p.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                                        p.is_foreign is true)
                   WHEN 0 THEN true
                   ELSE false END
                    is_pure,
               count(distinct p.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                                   (p.is_foreign is not true OR p.id = 54))
                    co_cooler_co_products,
               count(distinct p.id) FILTER ( WHERE ap.scene_type = '1' AND ap.sub_scene_type = '1' AND
                                                   (p.is_foreign is true OR p.id = 18))
                    co_cooler_non_co_products,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                              p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA')
                    stills_ss_water_unflavored_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                              p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA')
                    stills_ms_water_unflavored_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'SS%' AND
                              p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA')
                    stills_ss_water_unflavored_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'MS%' AND
                              p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA')
                    stills_ms_water_unflavored_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                              p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA')
                    stills_ss_water_flavored_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                              p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA')
                    stills_ms_water_flavored_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'SS%' AND
                              p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA')
                    stills_ss_water_flavored_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'MS%' AND
                              p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA')
                    stills_ms_water_flavored_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES')
                    stills_ss_ncbs_energy_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES')
                    stills_ms_ncbs_energy_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'SS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES')
                    stills_ss_ncbs_energy_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'MS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES')
                    stills_ms_ncbs_energy_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                              p.category = 'NCB' AND
                              p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS'))
                    stills_ss_ncbs_juice_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                              p.category = 'NCB' AND
                              p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS'))
                    stills_ms_ncbs_juice_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'SS%' AND
                              p.category = 'NCB' AND
                              p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS'))
                    stills_ss_ncbs_juice_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'MS%' AND
                              p.category = 'NCB' AND
                              p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS'))
                    stills_ms_ncbs_juice_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK')
                    stills_ss_ncbs_sports_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK')
                    stills_ms_ncbs_sports_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'SS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK')
                    stills_ss_ncbs_sports_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.group like 'MS%' AND
                              p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK')
                    stills_ms_ncbs_sports_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group = 'SS RET')
                    ssd_ss_ret_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group = 'SS RET')
                    ssd_ss_ret_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group = 'SS OW')
                    ssd_ss_ow_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group = 'SS OW')
                    ssd_ss_ow_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group like 'SS%' AND p.flavour_name = 'Cola')
                    ssd_ss_cola_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group like 'SS%' AND p.flavour_name = 'Cola')
                    ssd_ss_cola_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group like 'SS%' AND p.flavour_name != 'Cola')
                    ssd_ss_flavor_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group like 'SS%' AND p.flavour_name != 'Cola')
                    ssd_ss_flavor_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group = 'MS RET')
                    ssd_ms_ret_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group = 'MS RET')
                    ssd_ms_ret_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group = 'MS OW')
                    ssd_ms_ow_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group = 'MS OW')
                    ssd_ms_ow_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group like 'MS%' AND p.flavour_name = 'Cola')
                    ssd_ms_cola_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group like 'MS%' AND p.flavour_name = 'Cola')
                    ssd_ms_cola_pe,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                              p.group like 'MS%' AND p.flavour_name != 'Cola')
                    ssd_ms_flavor_co,
               count(distinct p.id)
               FILTER ( WHERE p.is_foreign is true AND p.category = 'SSD' AND
                              p.group like 'MS%' AND p.flavour_name != 'Cola')
                    ssd_ms_flavor_pe,
               s.id survey_id
        FROM survey s
                 INNER JOIN analyzed_photo ap on s.id = ap.survey_id
                 INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
                 INNER JOIN product p on rp.product_id = p.id
        GROUP BY s.id
    )
INSERT
INTO preprocessed_ir (is_pure,
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
                      essential_facings,
                      required_essential_facings,
                      success_photo_facings,
                      required_success_photo_facings,
                      survey_id)
SELECT ps.is_pure,
       ps.co_cooler_co_products,
       ps.co_cooler_non_co_products,
       ps.stills_ss_water_unflavored_co,
       ps.stills_ms_water_unflavored_co,
       ps.stills_ss_water_unflavored_pe,
       ps.stills_ms_water_unflavored_pe,
       ps.stills_ss_water_flavored_co,
       ps.stills_ms_water_flavored_co,
       ps.stills_ss_water_flavored_pe,
       ps.stills_ms_water_flavored_pe,
       ps.stills_ss_ncbs_energy_co,
       ps.stills_ms_ncbs_energy_co,
       ps.stills_ss_ncbs_energy_pe,
       ps.stills_ms_ncbs_energy_pe,
       ps.stills_ss_ncbs_juice_co,
       ps.stills_ms_ncbs_juice_co,
       ps.stills_ss_ncbs_juice_pe,
       ps.stills_ms_ncbs_juice_pe,
       ps.stills_ss_ncbs_sports_co,
       ps.stills_ms_ncbs_sports_co,
       ps.stills_ss_ncbs_sports_pe,
       ps.stills_ms_ncbs_sports_pe,
       ps.ssd_ss_ret_co,
       ps.ssd_ss_ret_pe,
       ps.ssd_ss_ow_co,
       ps.ssd_ss_ow_pe,
       ps.ssd_ss_cola_co,
       ps.ssd_ss_cola_pe,
       ps.ssd_ss_flavor_co,
       ps.ssd_ss_flavor_pe,
       ps.ssd_ms_ret_co,
       ps.ssd_ms_ret_pe,
       ps.ssd_ms_ow_co,
       ps.ssd_ms_ow_pe,
       ps.ssd_ms_cola_co,
       ps.ssd_ms_cola_pe,
       ps.ssd_ms_flavor_co,
       ps.ssd_ms_flavor_pe,
       ac.essential_facings,
       ac.required_essential_facings,
       ac.success_photo_facings,
       ac.required_success_photo_facings,
       ac.survey_id
FROM product_sums ps
         INNER JOIN aggregated_compliance ac on ac.survey_id = ps.survey_id
ON CONFLICT (survey_id) DO UPDATE SET is_pure                        = excluded.is_pure,
                                      co_cooler_co_products          = excluded.co_cooler_co_products,
                                      co_cooler_non_co_products      = excluded.co_cooler_non_co_products,
                                      stills_ss_water_unflavored_co  = excluded.stills_ss_water_unflavored_co,
                                      stills_ms_water_unflavored_co  = excluded.stills_ms_water_unflavored_co,
                                      stills_ss_water_unflavored_pe  = excluded.stills_ss_water_unflavored_pe,
                                      stills_ms_water_unflavored_pe  = excluded.stills_ms_water_unflavored_pe,
                                      stills_ss_water_flavored_co    = excluded.stills_ss_water_flavored_co,
                                      stills_ms_water_flavored_co    = excluded.stills_ms_water_flavored_co,
                                      stills_ss_water_flavored_pe    = excluded.stills_ss_water_flavored_pe,
                                      stills_ms_water_flavored_pe    = excluded.stills_ms_water_flavored_pe,
                                      stills_ss_ncbs_energy_co       = excluded.stills_ss_ncbs_energy_co,
                                      stills_ms_ncbs_energy_co       = excluded.stills_ms_ncbs_energy_co,
                                      stills_ss_ncbs_energy_pe       = excluded.stills_ss_ncbs_energy_pe,
                                      stills_ms_ncbs_energy_pe       = excluded.stills_ms_ncbs_energy_pe,
                                      stills_ss_ncbs_juice_co        = excluded.stills_ss_ncbs_juice_co,
                                      stills_ms_ncbs_juice_co        = excluded.stills_ms_ncbs_juice_co,
                                      stills_ss_ncbs_juice_pe        = excluded.stills_ss_ncbs_juice_pe,
                                      stills_ms_ncbs_juice_pe        = excluded.stills_ms_ncbs_juice_pe,
                                      stills_ss_ncbs_sports_co       = excluded.stills_ss_ncbs_sports_co,
                                      stills_ms_ncbs_sports_co       = excluded.stills_ms_ncbs_sports_co,
                                      stills_ss_ncbs_sports_pe       = excluded.stills_ss_ncbs_sports_pe,
                                      stills_ms_ncbs_sports_pe       = excluded.stills_ms_ncbs_sports_pe,
                                      ssd_ss_ret_co                  = excluded.ssd_ss_ret_co,
                                      ssd_ss_ret_pe                  = excluded.ssd_ss_ret_pe,
                                      ssd_ss_ow_co                   = excluded.ssd_ss_ow_co,
                                      ssd_ss_ow_pe                   = excluded.ssd_ss_ow_pe,
                                      ssd_ss_cola_co                 = excluded.ssd_ss_cola_co,
                                      ssd_ss_cola_pe                 = excluded.ssd_ss_cola_pe,
                                      ssd_ss_flavor_co               = excluded.ssd_ss_flavor_co,
                                      ssd_ss_flavor_pe               = excluded.ssd_ss_flavor_pe,
                                      ssd_ms_ret_co                  = excluded.ssd_ms_ret_co,
                                      ssd_ms_ret_pe                  = excluded.ssd_ms_ret_pe,
                                      ssd_ms_ow_co                   = excluded.ssd_ms_ow_co,
                                      ssd_ms_ow_pe                   = excluded.ssd_ms_ow_pe,
                                      ssd_ms_cola_co                 = excluded.ssd_ms_cola_co,
                                      ssd_ms_cola_pe                 = excluded.ssd_ms_cola_pe,
                                      ssd_ms_flavor_co               = excluded.ssd_ms_flavor_co,
                                      ssd_ms_flavor_pe               = excluded.ssd_ms_flavor_pe,
                                      essential_facings              = excluded.essential_facings,
                                      required_essential_facings     = excluded.required_essential_facings,
                                      success_photo_facings          = excluded.success_photo_facings,
                                      required_success_photo_facings = excluded.required_success_photo_facings

    ;
$$;
