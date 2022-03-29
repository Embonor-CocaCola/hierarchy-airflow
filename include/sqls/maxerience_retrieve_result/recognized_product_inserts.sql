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
    SELECT id,
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
    FROM tmp_recognized_product_typed input_rows
             INNER JOIN product p ON input_rows.product_id = p.id
             INNER JOIN survey s ON input_rows.survey_id :: uuid = s.id
             INNER JOIN analyzed_photo ap ON input_rows.analyzed_photo_id ::uuid = ap.id
        --     LEFT JOIN recognized_product target ON
        --        target.analyzed_photo_id = input_rows.analyzed_photo_id::uuid
        --    AND target.survey_id = input_rows.survey_id::uuid
        --    AND target.re_id = input_rows.re_id::text
        --    AND target.position::jsonb = input_rows.position::jsonb
        --    AND target.external_id = input_rows.external_id ::integer
        --    AND target.block_id = input_rows.block_id ::text
        --    AND target.product_id = input_rows.product_id::integer
        --    AND target.single_facings = input_rows.single_facings::integer
        --    AND target.is_foreign = input_rows.is_foreign::boolean
   -- WHERE target.id IS NULL
);
