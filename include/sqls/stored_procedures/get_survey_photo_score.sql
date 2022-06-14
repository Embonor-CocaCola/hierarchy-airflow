-- WARNING: Be careful when updating this function because it is called to populate a materialized
-- view for Expos-Service. If you change a column name, be sure to also change it in the code!
CREATE OR REPLACE FUNCTION get_survey_photo_score()
    RETURNS TABLE
            (
                survey_id        uuid,
                score_company    float4,
                score_competitor float4
            )
AS
$$
DECLARE
    config jsonb;
BEGIN
    select content from setting where name = 'surveySamplingConfig' into config;

    RETURN QUERY
        SELECT s.id survey_id,
               coalesce(
                                   (config -> 'factorWeightsCompany' ->> 'foreignAmount')::float4 / 100.0 *
                                   pe.co_cooler_foreign_products /
                                   nullif(pe.co_cooler_total_products, 0)
                           +
                                   (config -> 'factorWeightsCompany' ->>
                                    'emptyAmount')::float4 / 100.0 *
                                   pe.co_cooler_empty_products /
                                   nullif(pe.co_cooler_total_products, 0), 0
                   )::float4,
               coalesce(
                                   (config -> 'factorWeightsCompetitor' ->> 'foreignAmount')::float4 / 100.0 *
                                   pe.pe_cooler_foreign_products /
                                   nullif(pe.pe_cooler_total_products, 0)
                           +
                                   (config ->
                                    'factorWeightsCompetitor' ->>
                                    'emptyAmount')::float4 / 100.0 *
                                   pe.pe_cooler_empty_products /
                                   nullif(pe.pe_cooler_total_products, 0), 0
                   )::float4
        FROM survey s
                 inner join preprocessed_edf pe on pe.survey_id = s.id
                 inner join survey_metadata sm on sm.survey_id = s.id;
END;
$$
    LANGUAGE 'plpgsql';
