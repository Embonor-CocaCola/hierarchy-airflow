DROP PROCEDURE IF EXISTS calculate_survey_metadata();
CREATE OR REPLACE PROCEDURE calculate_survey_metadata()
    LANGUAGE SQL AS $$
        INSERT INTO survey_metadata (
            foreign_value,
            empty_value,
            ir_photos,
            days_since_last_survey,
            ambient_company_photos,
            ambient_competitor_photos,
            cooler_company_photos,
            cooler_competitor_photos,
            survey_id
        )
        SELECT
            (ps.unrecognized_products::float4 / nullif(ps.total_products, 0))::float4 foreign_value,
            (ps.empty_products::float4 / nullif(ps.total_products, 0))::float4 foreign_value,
            sum(array_length(a.attachments, 1)) filter (where q.heading like 'Fotos%' or q.heading ilike '%cuatripendón%'),
            s.created_at::date - (select s2.created_at::date from survey s2 where s2.customer_id = s.customer_id and s2.created_at < s.created_at order by s2.created_at DESC limit 1) days_since_last_survey,
            coalesce(sum(array_length(a.attachments, 1)) filter (where q.heading ilike 'Fotos%ambiente%Embonor%'),0),
            coalesce(sum(array_length(a.attachments, 1)) filter (where q.heading ilike 'Fotos%ambiente%competencia%'),0),
            coalesce(sum(array_length(a.attachments, 1)) filter (where q.heading ilike 'Fotos%frío%embonor%'),0),
            coalesce(sum(array_length(a.attachments, 1)) filter (where q.heading ilike 'Fotos%frío%competencia%'),0),
            s.id survey_id
        FROM survey s
            INNER JOIN preprocessed_sovi ps on s.id = ps.survey_id
            INNER JOIN answer a on a.survey_id = s.id
            INNER JOIN question q on q.id = a.question_id
            LEFT JOIN survey_metadata sm on sm.survey_id = s.id
        WHERE sm.id IS NULL
        GROUP BY s.id, ps.unrecognized_products, ps.total_products, ps.empty_products
;
$$;
