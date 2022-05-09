-- WARNING: Be careful when updating this function because it is called to populate two materialized
-- views for Expos-Service. If you change a column name, be sure to also change it in the code!
CREATE OR REPLACE FUNCTION get_sovi_calculations()
    RETURNS TABLE
            (
                ss_water_unflavored_co    smallint,
                ms_water_unflavored_co    smallint,
                ss_water_unflavored_total smallint,
                ms_water_unflavored_total smallint,
                ss_water_flavored_co      smallint,
                ms_water_flavored_co      smallint,
                ss_water_flavored_total   smallint,
                ms_water_flavored_total   smallint,
                ss_ncbs_energy_co         smallint,
                ms_ncbs_energy_co         smallint,
                ss_ncbs_energy_total      smallint,
                ms_ncbs_energy_total      smallint,
                ss_ncbs_juice_co          smallint,
                ms_ncbs_juice_co          smallint,
                ss_ncbs_juice_total       smallint,
                ms_ncbs_juice_total       smallint,
                ss_ncbs_sports_co         smallint,
                ms_ncbs_sports_co         smallint,
                ss_ncbs_sports_total      smallint,
                ms_ncbs_sports_total      smallint,
                ss_ssd_ret_co             smallint,
                ss_ssd_ret_total          smallint,
                ss_ssd_ow_co              smallint,
                ss_ssd_ow_total           smallint,
                ss_ssd_cola_co            smallint,
                ss_ssd_cola_total         smallint,
                ss_ssd_flavor_co          smallint,
                ss_ssd_flavor_total       smallint,
                ms_ssd_ret_co             smallint,
                ms_ssd_ret_total          smallint,
                ms_ssd_ow_co              smallint,
                ms_ssd_ow_total           smallint,
                ms_ssd_cola_co            smallint,
                ms_ssd_cola_total         smallint,
                ms_ssd_flavor_co          smallint,
                ms_ssd_flavor_total       smallint,
                survey_id                 uuid
            )
AS
$$
BEGIN
    RETURN QUERY
        SELECT COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                                       p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA'), 0)::smallint
                    ss_water_unflavored_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                                       p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA'), 0)::smallint
                    ms_water_unflavored_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'SS%' AND
                                       p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA'), 0)::smallint
                    ss_water_unflavored_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'MS%' AND
                                       p.category = 'AGUA' AND p.local_category_name != 'SABORIZADA'), 0)::smallint
                    ms_water_unflavored_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                                       p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA'), 0)::smallint
                    ss_water_flavored_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                                       p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA'), 0)::smallint
                    ms_water_flavored_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'SS%' AND
                                       p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA'), 0)::smallint
                    ss_water_flavored_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'MS%' AND
                                       p.category = 'AGUA' AND p.local_category_name = 'SABORIZADA'), 0)::smallint
                    ms_water_flavored_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES'), 0)::smallint
                    ss_ncbs_energy_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES'), 0)::smallint
                    ms_ncbs_energy_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'SS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES'), 0)::smallint
                    ss_ncbs_energy_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'MS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'ENERGIZANTES'), 0)::smallint
                    ms_ncbs_energy_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                                       p.category = 'NCB' AND
                                       p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS')), 0)::smallint
                    ss_ncbs_juice_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                                       p.category = 'NCB' AND
                                       p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS')), 0)::smallint
                    ms_ncbs_juice_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'SS%' AND
                                       p.category = 'NCB' AND
                                       p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS')), 0)::smallint
                    ss_ncbs_juice_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'MS%' AND
                                       p.category = 'NCB' AND
                                       p.local_category_name IN ('JUGOS', 'KAPO', 'LACTEOS')), 0)::smallint
                    ms_ncbs_juice_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'SS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK'), 0)::smallint
                    ss_ncbs_sports_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.group like 'MS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK'), 0)::smallint
                    ms_ncbs_sports_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'SS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK'), 0)::smallint
                    ss_ncbs_sports_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.group like 'MS%' AND
                                       p.category = 'NCB' AND p.local_category_name = 'SPORT DRINK'), 0)::smallint
                    ms_ncbs_sports_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group = 'SS RET'), 0)::smallint
                    ss_ssd_ret_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group = 'SS RET'), 0)::smallint
                    ss_ssd_ret_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group = 'SS OW'), 0)::smallint
                    ss_ssd_ow_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group = 'SS OW'), 0)::smallint
                    ss_ssd_ow_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group like 'SS%' AND p.flavour_name = 'Cola'), 0)::smallint
                    ss_ssd_cola_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group like 'SS%' AND p.flavour_name = 'Cola'), 0)::smallint
                    ss_ssd_cola_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group like 'SS%' AND p.flavour_name != 'Cola'), 0)::smallint
                    ss_ssd_flavor_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group like 'SS%' AND p.flavour_name != 'Cola'), 0)::smallint
                    ss_ssd_flavor_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group = 'MS RET'), 0)::smallint
                    ms_ssd_ret_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group = 'MS RET'), 0)::smallint
                    ms_ssd_ret_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group = 'MS OW'), 0)::smallint
                    ms_ssd_ow_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group = 'MS OW'), 0)::smallint
                    ms_ssd_ow_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group like 'MS%' AND p.flavour_name = 'Cola'), 0)::smallint
                    ms_ssd_cola_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group like 'MS%' AND p.flavour_name = 'Cola'), 0)::smallint
                    ms_ssd_cola_total,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.is_foreign is not true AND p.category = 'SSD' AND
                                       p.group like 'MS%' AND p.flavour_name != 'Cola'), 0)::smallint
                    ms_ssd_flavor_co,
               COALESCE(count(distinct p.id)
                        FILTER ( WHERE p.category = 'SSD' AND
                                       p.group like 'MS%' AND p.flavour_name != 'Cola'), 0)::smallint
                    ms_ssd_flavor_total,
               s.id survey_id
        FROM survey s
                 INNER JOIN analyzed_photo ap on s.id = ap.survey_id
                 INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
                 INNER JOIN product p on rp.product_id = p.id
        GROUP BY s.id;
END;
$$
    LANGUAGE 'plpgsql';
