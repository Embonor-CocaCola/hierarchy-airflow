-- WARNING: Be careful when updating this function because it is called to populate two materialized
-- views for Expos-Service. If you change a column name, be sure to also change it in the code!
    CREATE OR REPLACE FUNCTION get_aggregated_compliance(only_essentials BOOLEAN)
        RETURNS TABLE
                (
                    facings                 numeric,
                    req_facings             numeric,
                    ss_ssd_ow               numeric,
                    req_ss_ssd_ow           numeric,
                    ms_ssd_ow               numeric,
                    req_ms_ssd_ow           numeric,
                    ss_ssd_ret              numeric,
                    req_ss_ssd_ret          numeric,
                    ms_ssd_ret              numeric,
                    req_ms_ssd_ret          numeric,
                    ss_ssd_cola             numeric,
                    req_ss_ssd_cola         numeric,
                    ms_ssd_cola             numeric,
                    req_ms_ssd_cola         numeric,
                    ss_ssd_flavor           numeric,
                    req_ss_ssd_flavor       numeric,
                    ms_ssd_flavor           numeric,
                    req_ms_ssd_flavor       numeric,
                    ss_water_unflavored     numeric,
                    req_ss_water_unflavored numeric,
                    ms_water_unflavored     numeric,
                    req_ms_water_unflavored numeric,
                    ss_water_flavored       numeric,
                    req_ss_water_flavored   numeric,
                    ms_water_flavored       numeric,
                    req_ms_water_flavored   numeric,
                    ss_ncbs_energy          numeric,
                    req_ss_ncbs_energy      numeric,
                    ms_ncbs_energy          numeric,
                    req_ms_ncbs_energy      numeric,
                    ss_ncbs_sports          numeric,
                    req_ss_ncbs_sports      numeric,
                    ms_ncbs_sports          numeric,
                    req_ms_ncbs_sports      numeric,
                    ss_ncbs_juice           numeric,
                    req_ss_ncbs_juice       numeric,
                    ms_ncbs_juice           numeric,
                    req_ms_ncbs_juice       numeric,
                    survey_id               uuid
                )
    AS
    $$
    BEGIN
        RETURN QUERY SELECT sum(sfc.present_facings)::numeric                                      facings,
                            sum(sfc.required_facings)::numeric                                     req_facings,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'SS OW' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ss_ssd_ow,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'SS OW' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   req_ss_ssd_ow,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'MS OW' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ms_ssd_ow,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'MS OW' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   req_ms_ssd_ow,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'SS RET' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ss_ssd_ret,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'SS RET' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   req_ss_ssd_ret,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'MS RET' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ms_ssd_ret,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'MS RET' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   req_ms_ssd_ret,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::numeric             ss_ssd_cola,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::numeric             req_ss_ssd_cola,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::numeric             ms_ssd_cola,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::numeric             req_ms_ssd_cola,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::numeric         ss_ssd_flavor,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::numeric         req_ss_ssd_flavor,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::numeric         ms_ssd_flavor,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::numeric         req_ms_ssd_flavor,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ), 0)::numeric                     ss_water_unflavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ),
                                     0)::numeric                                                   req_ss_water_unflavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ), 0)::numeric                     ms_water_unflavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ),
                                     0)::numeric                                                   req_ms_water_unflavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ), 0)::numeric                    ss_water_flavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ),
                                     0)::numeric                                                   req_ss_water_flavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ), 0)::numeric                    ms_water_flavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ),
                                     0)::numeric                                                   req_ms_water_flavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::numeric                  ss_ncbs_energy,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::numeric                  req_ss_ncbs_energy,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::numeric                  ms_ncbs_energy,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::numeric                  req_ms_ncbs_energy,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::numeric                   ss_ncbs_sports,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::numeric                   req_ss_ncbs_sports,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::numeric                   ms_ncbs_sports,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::numeric                   req_ms_ncbs_sports,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::numeric ss_ncbs_juice,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::numeric req_ss_ncbs_juice,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::numeric ms_ncbs_juice,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::numeric req_ms_ncbs_juice,
                            sfc.survey_id
                     FROM sku_family_compliance sfc
                              inner join success_photo_product spp on sfc.success_photo_product_id = spp.id
                     WHERE only_essentials is false
                        OR sfc.is_essential is true
                     GROUP BY sfc.survey_id;
    END;
    $$
        LANGUAGE 'plpgsql';
