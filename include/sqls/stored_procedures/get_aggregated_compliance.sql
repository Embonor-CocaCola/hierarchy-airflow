-- WARNING: Be careful when updating this function because it is called to populate two materialized
-- views for Expos-Service. If you change a column name, be sure to also change it in the code!

    BEGIN;

    DROP FUNCTION get_aggregated_compliance(only_essentials BOOLEAN) CASCADE;

    DROP MATERIALIZED VIEW IF EXISTS public.preprocessed_essentials CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS public.preprocessed_success_photo CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS airflow.preprocessed_essentials CASCADE;
    DROP MATERIALIZED VIEW IF EXISTS airflow.preprocessed_success_photo CASCADE;

    CREATE OR REPLACE FUNCTION get_aggregated_compliance(only_essentials BOOLEAN)
        RETURNS TABLE
                (
                    facings                 numeric,
                    req_facings             smallint,
                    ss_ssd_ow               numeric,
                    req_ss_ssd_ow           smallint,
                    ms_ssd_ow               numeric,
                    req_ms_ssd_ow           smallint,
                    ss_ssd_ret              numeric,
                    req_ss_ssd_ret          smallint,
                    ms_ssd_ret              numeric,
                    req_ms_ssd_ret          smallint,
                    ss_ssd_cola             numeric,
                    req_ss_ssd_cola         smallint,
                    ms_ssd_cola             numeric,
                    req_ms_ssd_cola         smallint,
                    ss_ssd_flavor           numeric,
                    req_ss_ssd_flavor       smallint,
                    ms_ssd_flavor           numeric,
                    req_ms_ssd_flavor       smallint,
                    ss_water_unflavored     numeric,
                    req_ss_water_unflavored smallint,
                    ms_water_unflavored     numeric,
                    req_ms_water_unflavored smallint,
                    ss_water_flavored       numeric,
                    req_ss_water_flavored   smallint,
                    ms_water_flavored       numeric,
                    req_ms_water_flavored   smallint,
                    ss_ncbs_energy          numeric,
                    req_ss_ncbs_energy      smallint,
                    ms_ncbs_energy          numeric,
                    req_ms_ncbs_energy      smallint,
                    ss_ncbs_sports          numeric,
                    req_ss_ncbs_sports      smallint,
                    ms_ncbs_sports          numeric,
                    req_ms_ncbs_sports      smallint,
                    ss_ncbs_juice           numeric,
                    req_ss_ncbs_juice       smallint,
                    ms_ncbs_juice           numeric,
                    req_ms_ncbs_juice       smallint,
                    survey_id               uuid
                )
    AS
    $$
    BEGIN
        RETURN QUERY SELECT sum(sfc.present_facings)::numeric                                      facings,
                            sum(sfc.required_facings)::smallint                                     req_facings,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'SS OW' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ss_ssd_ow,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'SS OW' AND spp.product_category = 'SSD' ),
                                     0)::smallint                                                   req_ss_ssd_ow,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'MS OW' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ms_ssd_ow,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'MS OW' AND spp.product_category = 'SSD' ),
                                     0)::smallint                                                   req_ms_ssd_ow,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'SS RET' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ss_ssd_ret,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'SS RET' AND spp.product_category = 'SSD' ),
                                     0)::smallint                                                   req_ss_ssd_ret,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group = 'MS RET' AND spp.product_category = 'SSD' ),
                                     0)::numeric                                                   ms_ssd_ret,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group = 'MS RET' AND spp.product_category = 'SSD' ),
                                     0)::smallint                                                   req_ms_ssd_ret,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::numeric             ss_ssd_cola,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::smallint             req_ss_ssd_cola,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::numeric             ms_ssd_cola,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS TRUE ), 0)::smallint             req_ms_ssd_cola,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::numeric         ss_ssd_flavor,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::smallint         req_ss_ssd_flavor,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::numeric         ms_ssd_flavor,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'SSD' AND
                                                    spp.is_cola IS NOT TRUE ), 0)::smallint         req_ms_ssd_flavor,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ), 0)::numeric                     ss_water_unflavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ),
                                     0)::smallint                                                   req_ss_water_unflavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ), 0)::numeric                     ms_water_unflavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SIN SABOR' ),
                                     0)::smallint                                                   req_ms_water_unflavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ), 0)::numeric                    ss_water_flavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ),
                                     0)::smallint                                                   req_ss_water_flavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ), 0)::numeric                    ms_water_flavored,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'AGUA' AND
                                                    spp.sub_category =
                                                    'SABORIZADA' ),
                                     0)::smallint                                                   req_ms_water_flavored,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::numeric                  ss_ncbs_energy,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::smallint                  req_ss_ncbs_energy,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::numeric                  ms_ncbs_energy,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'ENERGIZANTES' ), 0)::smallint                  req_ms_ncbs_energy,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::numeric                   ss_ncbs_sports,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::smallint                   req_ss_ncbs_sports,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::numeric                   ms_ncbs_sports,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category =
                                                    'SPORT DRINK' ), 0)::smallint                   req_ms_ncbs_sports,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::numeric ss_ncbs_juice,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'SS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::smallint req_ss_ncbs_juice,
                            COALESCE(sum(sfc.present_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::numeric ms_ncbs_juice,
                            COALESCE(sum(sfc.required_facings)
                                     filter ( where spp.product_group like 'MS%' AND spp.product_category = 'NCB' AND
                                                    spp.sub_category IN ('JUGOS', 'KAPO',
                                                                         'LACTEOS') ), 0)::smallint req_ms_ncbs_juice,
                            sfc.survey_id
                     FROM sku_family_compliance sfc
                              inner join success_photo_product spp on sfc.success_photo_product_id = spp.id
                     WHERE only_essentials is false
                        OR sfc.is_essential is true
                     GROUP BY sfc.survey_id;
    END;
    $$
        LANGUAGE 'plpgsql';

    CREATE MATERIALIZED VIEW public.preprocessed_success_photo AS SELECT * FROM get_aggregated_compliance(false);
    CREATE UNIQUE INDEX uidx_preprocessed_success_photo_survey_id ON public.preprocessed_success_photo(survey_id);

    CREATE MATERIALIZED VIEW public.preprocessed_essentials AS SELECT * FROM get_aggregated_compliance(true);
    CREATE UNIQUE INDEX uidx_preprocessed_essentials_survey_id ON public.preprocessed_essentials(survey_id);

    COMMIT;
