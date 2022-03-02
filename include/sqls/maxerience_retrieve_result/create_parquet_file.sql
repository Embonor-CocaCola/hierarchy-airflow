INSERT INTO parquet_file (
    id,
    created_at,
    content_type,
    path
)
VALUES %s
ON CONFLICT(path) DO NOTHING
;
