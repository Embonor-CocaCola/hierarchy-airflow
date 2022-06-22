BEGIN;
    DROP MATERIALIZED VIEW IF EXISTS public.sku_family_compliance CASCADE;

    DROP FUNCTION IF EXISTS get_sku_family_compliance() CASCADE;

    CREATE OR REPLACE FUNCTION get_sku_family_compliance()
        RETURNS TABLE
                (
                    present_facings          smallint,
                    required_facings         smallint,
                    is_essential             boolean,
                    survey_id                uuid,
                    success_photo_product_id uuid
                )
    AS
    $$
    BEGIN
        RETURN QUERY
            with survey_cluster as (
                select s.id, c.cluster_id, s.skips_survey
                from survey s
                         inner join customer c on s.customer_id = c.id
            )
            SELECT CASE
                       WHEN spp.flavors > 1
                           THEN
                           LEAST(LEAST(count(distinct rp.product_id) filter (
                               where p.sku = ANY (spp.skus)
                               ), spp.flavors) * (spp.required_facings::decimal / spp.flavors), count(rp.id) filter (
                               where p.sku = ANY (spp.skus)
                               ))
                       ELSE
                           LEAST(count(rp.id) filter (
                               where p.sku = ANY (spp.skus)
                               ), spp.required_facings)
                       END present_facings,
                   spp.required_facings,
                   spp.is_essential,
                   s.id    survey_id,
                   spp.id  success_photo_product_id
            FROM survey_cluster s
                     INNER JOIN analyzed_photo ap on s.id = ap.survey_id
                     INNER JOIN recognized_product rp on ap.id = rp.analyzed_photo_id
                     INNER JOIN product p on rp.product_id = p.id
                     INNER JOIN success_photo_product spp on spp.cluster_id = s.cluster_id
            WHERE s.skips_survey IS NOT TRUE
            GROUP BY s.id, spp.id;
    END;
    $$ language 'plpgsql';

    CREATE MATERIALIZED VIEW sku_family_compliance AS SELECT * FROM get_sku_family_compliance();
    CREATE UNIQUE INDEX uidx_sku_family_compliance_survey_id_spp_id ON sku_family_compliance(survey_id, success_photo_product_id);
COMMIT;
