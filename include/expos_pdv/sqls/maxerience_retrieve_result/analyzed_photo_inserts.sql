UPDATE analyzed_photo AS ap SET
    verified_on = a.verified_on,
    source = a.source,
    image_quality = a.image_quality::integer,
    created_on_time = a.created_on_time,
    last_modified_time = a.last_modified_time,
    file_created_time = a.file_created_time,
    external_id = a.external_id::integer,
    parquet_file_id = a.parquet_file_id::uuid
FROM tmp_analyzed_photo_typed a
where a.id::text = ap.id::text
and
(
    ap.verified_on IS DISTINCT FROM a.verified_on OR
    ap.source IS DISTINCT FROM a.source OR
    ap.image_quality IS DISTINCT FROM a.image_quality::integer OR
    ap.created_on_time IS DISTINCT FROM a.created_on_time OR
    ap.last_modified_time IS DISTINCT FROM a.last_modified_time OR
    ap.file_created_time IS DISTINCT FROM a.file_created_time OR
    ap.external_id IS DISTINCT FROM a.external_id::integer
)
;
