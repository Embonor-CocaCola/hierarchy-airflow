CREATE OR REPLACE PROCEDURE calculate_ir_based_data()
    LANGUAGE SQL AS
$$
with aggregated_compliance AS (
    select sum(sfc.present_facings) filter ( where sfc.is_essential is true )                         essential_facings,
           sum(sfc.required_facings) filter ( where sfc.is_essential is true )                        required_essential_facings,
           sum(sfc.present_facings)                                                                   success_photo_facings,
           sum(sfc.required_facings)                                                                  required_success_photo_facings,
           sum(sfc.present_facings)
           filter ( where spp.product_group = 'SS OW' AND spp.product_category = 'SSD' )              sp_ss_ow_ssd,
           sum(sfc.required_facings)
           filter ( where spp.product_group = 'SS OW' AND spp.product_category = 'SSD' )              req_sp_ss_ow_ssd,
           sum(sfc.present_facings)
           filter ( where spp.product_group = 'MS OW' AND spp.product_category = 'SSD' )              sp_ms_ow_ssd,
           sum(sfc.required_facings)
           filter ( where spp.product_group = 'MS OW' AND spp.product_category = 'SSD' )              req_sp_ms_ow_ssd,
           sum(sfc.present_facings)
           filter ( where spp.product_group = 'SS RET' AND spp.product_category = 'SSD' )             sp_ss_ret_ssd,
           sum(sfc.required_facings)
           filter ( where spp.product_group = 'SS RET' AND spp.product_category = 'SSD' )             req_sp_ss_ret_ssd,
           sum(sfc.present_facings)
           filter ( where spp.product_group = 'MS RET' AND spp.product_category = 'SSD' )             sp_ms_ret_ssd,
           sum(sfc.required_facings)
           filter ( where spp.product_group = 'MS RET' AND spp.product_category = 'SSD' )             req_sp_ms_ret_ssd,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                   spp.is_cola IS TRUE )                              sp_ss_cola_ssd,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE )                             req_sp_ss_cola_ssd,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                   spp.is_cola IS TRUE )                              sp_ms_cola_ssd,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE )                             req_sp_ms_cola_ssd,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                   spp.is_cola IS NOT TRUE )                          sp_ss_flavor_ssd,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE )                         req_sp_ss_flavor_ssd,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                   spp.is_cola IS NOT TRUE )                          sp_ms_flavor_ssd,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE )                         req_sp_ms_flavor_ssd,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                   spp.sub_category =
                                                   'SIN SABOR' )                                      sp_ss_waters_unflavored,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' )                                     req_sp_ss_waters_unflavored,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                   spp.sub_category =
                                                   'SIN SABOR' )                                      sp_ms_waters_unflavored,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' )                                     req_sp_ms_waters_unflavored,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                   spp.sub_category =
                                                   'SABORIZADA' )                                     sp_ss_waters_flavored,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' )                                    req_sp_ss_waters_flavored,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                   spp.sub_category =
                                                   'SABORIZADA' )                                     sp_ms_waters_flavored,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' )                                    req_sp_ms_waters_flavored,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                   spp.sub_category = 'ENERGIZANTES' )                sp_ss_ncbs_energy,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' )                                  req_sp_ss_ncbs_energy,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                   spp.sub_category = 'ENERGIZANTES' )                sp_ms_ncbs_energy,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' )                                  req_sp_ms_ncbs_energy,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                   spp.sub_category = 'SPORT DRINK' )                 sp_ss_ncbs_sports,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' )                                   req_sp_ss_ncbs_sports,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                   spp.sub_category = 'SPORT DRINK' )                 sp_ms_ncbs_sports,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' )                                   req_sp_ms_ncbs_sports,
           sum(sfc.present_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                   spp.sub_category IN ('JUGOS', 'KAPO', 'LACTEOS') ) sp_ss_ncbs_juice,
           sum(sfc.required_facings) filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') )                 req_sp_ss_ncbs_juice,
           sum(sfc.present_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                   spp.sub_category IN ('JUGOS', 'KAPO', 'LACTEOS') ) sp_ms_ncbs_juice,
           sum(sfc.required_facings) filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') )                 req_sp_ms_ncbs_juice,
           sfc.survey_id
    from sku_family_compliance sfc
             inner join success_photo_product spp on sfc.success_photo_product_id = spp.id
    group by sfc.survey_id
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
                      sp_ss_ow_ssd,
                      req_sp_ss_ow_ssd,
                      sp_ms_ow_ssd,
                      req_sp_ms_ow_ssd,
                      sp_ss_ret_ssd,
                      req_sp_ss_ret_ssd,
                      sp_ms_ret_ssd,
                      req_sp_ms_ret_ssd,
                      sp_ss_cola_ssd,
                      req_sp_ss_cola_ssd,
                      sp_ms_cola_ssd,
                      req_sp_ms_cola_ssd,
                      sp_ss_flavor_ssd,
                      req_sp_ss_flavor_ssd,
                      sp_ms_flavor_ssd,
                      req_sp_ms_flavor_ssd,
                      sp_ss_waters_unflavored,
                      req_sp_ss_waters_unflavored,
                      sp_ms_waters_unflavored,
                      req_sp_ms_waters_unflavored,
                      sp_ss_waters_flavored,
                      req_sp_ss_waters_flavored,
                      sp_ms_waters_flavored,
                      req_sp_ms_waters_flavored,
                      sp_ss_ncbs_energy,
                      req_sp_ss_ncbs_energy,
                      sp_ms_ncbs_energy,
                      req_sp_ms_ncbs_energy,
                      sp_ss_ncbs_sports,
                      req_sp_ss_ncbs_sports,
                      sp_ms_ncbs_sports,
                      req_sp_ms_ncbs_sports,
                      sp_ss_ncbs_juice,
                      req_sp_ss_ncbs_juice,
                      sp_ms_ncbs_juice,
                      req_sp_ms_ncbs_juice,
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
       coalesce(ac.sp_ss_ow_ssd, 0),
       coalesce(ac.req_sp_ss_ow_ssd, 0),
       coalesce(ac.sp_ms_ow_ssd, 0),
       coalesce(ac.req_sp_ms_ow_ssd, 0),
       coalesce(ac.sp_ss_ret_ssd, 0),
       coalesce(ac.req_sp_ss_ret_ssd, 0),
       coalesce(ac.sp_ms_ret_ssd, 0),
       coalesce(ac.req_sp_ms_ret_ssd, 0),
       coalesce(ac.sp_ss_cola_ssd, 0),
       coalesce(ac.req_sp_ss_cola_ssd, 0),
       coalesce(ac.sp_ms_cola_ssd, 0),
       coalesce(ac.req_sp_ms_cola_ssd, 0),
       coalesce(ac.sp_ss_flavor_ssd, 0),
       coalesce(ac.req_sp_ss_flavor_ssd, 0),
       coalesce(ac.sp_ms_flavor_ssd, 0),
       coalesce(ac.req_sp_ms_flavor_ssd, 0),
       coalesce(ac.sp_ss_waters_unflavored, 0),
       coalesce(ac.req_sp_ss_waters_unflavored, 0),
       coalesce(ac.sp_ms_waters_unflavored, 0),
       coalesce(ac.req_sp_ms_waters_unflavored, 0),
       coalesce(ac.sp_ss_waters_flavored, 0),
       coalesce(ac.req_sp_ss_waters_flavored, 0),
       coalesce(ac.sp_ms_waters_flavored, 0),
       coalesce(ac.req_sp_ms_waters_flavored, 0),
       coalesce(ac.sp_ss_ncbs_energy, 0),
       coalesce(ac.req_sp_ss_ncbs_energy, 0),
       coalesce(ac.sp_ms_ncbs_energy, 0),
       coalesce(ac.req_sp_ms_ncbs_energy, 0),
       coalesce(ac.sp_ss_ncbs_sports, 0),
       coalesce(ac.req_sp_ss_ncbs_sports, 0),
       coalesce(ac.sp_ms_ncbs_sports, 0),
       coalesce(ac.req_sp_ms_ncbs_sports, 0),
       coalesce(ac.sp_ss_ncbs_juice, 0),
       coalesce(ac.req_sp_ss_ncbs_juice, 0),
       coalesce(ac.sp_ms_ncbs_juice, 0),
       coalesce(ac.req_sp_ms_ncbs_juice, 0),
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
                                      required_success_photo_facings = excluded.required_success_photo_facings,
                                      sp_ss_ow_ssd                   = excluded.sp_ss_ow_ssd,
                                      req_sp_ss_ow_ssd               = excluded.req_sp_ss_ow_ssd,
                                      sp_ms_ow_ssd                   = excluded.sp_ms_ow_ssd,
                                      req_sp_ms_ow_ssd               = excluded.req_sp_ms_ow_ssd,
                                      sp_ss_ret_ssd                  = excluded.sp_ss_ret_ssd,
                                      req_sp_ss_ret_ssd              = excluded.req_sp_ss_ret_ssd,
                                      sp_ms_ret_ssd                  = excluded.sp_ms_ret_ssd,
                                      req_sp_ms_ret_ssd              = excluded.req_sp_ms_ret_ssd,
                                      sp_ss_cola_ssd                 = excluded.sp_ss_cola_ssd,
                                      req_sp_ss_cola_ssd             = excluded.req_sp_ss_cola_ssd,
                                      sp_ms_cola_ssd                 = excluded.sp_ms_cola_ssd,
                                      req_sp_ms_cola_ssd             = excluded.req_sp_ms_cola_ssd,
                                      sp_ss_flavor_ssd               = excluded.sp_ss_flavor_ssd,
                                      req_sp_ss_flavor_ssd           = excluded.req_sp_ss_flavor_ssd,
                                      sp_ms_flavor_ssd               = excluded.sp_ms_flavor_ssd,
                                      req_sp_ms_flavor_ssd           = excluded.req_sp_ms_flavor_ssd,
                                      sp_ss_waters_unflavored        = excluded.sp_ss_waters_unflavored,
                                      req_sp_ss_waters_unflavored    = excluded.req_sp_ss_waters_unflavored,
                                      sp_ms_waters_unflavored        = excluded.sp_ms_waters_unflavored,
                                      req_sp_ms_waters_unflavored    = excluded.req_sp_ms_waters_unflavored,
                                      sp_ss_waters_flavored          = excluded.sp_ss_waters_flavored,
                                      req_sp_ss_waters_flavored      = excluded.req_sp_ss_waters_flavored,
                                      sp_ms_waters_flavored          = excluded.sp_ms_waters_flavored,
                                      req_sp_ms_waters_flavored      = excluded.req_sp_ms_waters_flavored,
                                      sp_ss_ncbs_energy              = excluded.sp_ss_ncbs_energy,
                                      req_sp_ss_ncbs_energy          = excluded.req_sp_ss_ncbs_energy,
                                      sp_ms_ncbs_energy              = excluded.sp_ms_ncbs_energy,
                                      req_sp_ms_ncbs_energy          = excluded.req_sp_ms_ncbs_energy,
                                      sp_ss_ncbs_sports              = excluded.sp_ss_ncbs_sports,
                                      req_sp_ss_ncbs_sports          = excluded.req_sp_ss_ncbs_sports,
                                      sp_ms_ncbs_sports              = excluded.sp_ms_ncbs_sports,
                                      req_sp_ms_ncbs_sports          = excluded.req_sp_ms_ncbs_sports,
                                      sp_ss_ncbs_juice               = excluded.sp_ss_ncbs_juice,
                                      req_sp_ss_ncbs_juice           = excluded.req_sp_ss_ncbs_juice,
                                      sp_ms_ncbs_juice               = excluded.sp_ms_ncbs_juice,
                                      req_sp_ms_ncbs_juice           = excluded.req_sp_ms_ncbs_juice

    ;
$$;
