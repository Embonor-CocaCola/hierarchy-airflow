INSERT INTO recognized_product (
    id,
    analyzed_photo_id,
    product_id,
    survey_id,
    position,
    external_id,
    block_id,
    door_index,
    single_facings,
    is_foreign,
    re_id,
    file_created_time
)(
    SELECT input_rows.id,
           input_rows.analyzed_photo_id,
           input_rows.product_id,
           input_rows.survey_id,
           input_rows.position::jsonb,
           input_rows.external_id,
           input_rows.block_id,
           input_rows.door_index,
           input_rows.single_facings,
           input_rows.is_foreign,
           input_rows.re_id,
           input_rows.file_created_time
    FROM (VALUES %s)
             AS input_rows(
                           id,
                           analyzed_photo_id,
                           product_id,
                           survey_id,
                           position,
                           external_id,
                           block_id,
                           door_index,
                           single_facings,
                           is_foreign,
                           re_id,
                           file_created_time
            )
             INNER JOIN product p ON input_rows.product_id = p.id
             INNER JOIN survey s ON input_rows.survey_id :: uuid = s.id
             INNER JOIN analyzed_photo ap ON input_rows.analyzed_photo_id ::uuid = ap.id
             LEFT JOIN recognized_product target ON
                target.analyzed_photo_id = input_rows.analyzed_photo_id
            AND target.survey_id = input_rows.survey_id
            AND target.re_id = input_rows.re_id
            AND target.position::jsonb = input_rows.position::jsonb
            AND target.external_id = input_rows.external_id
            AND target.block_id = input_rows.block_id
            AND target.product_id = input_rows.product_id
            AND target.single_facings = input_rows.single_facings
            AND target.is_foreign = input_rows.is_foreign
    WHERE target.id IS NULL
);
