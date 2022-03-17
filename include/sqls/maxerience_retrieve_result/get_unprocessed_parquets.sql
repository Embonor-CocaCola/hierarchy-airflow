select id, path, created_at from parquet_file where content_type = %(content_type)s and processed_at IS NULL ORDER BY created_at ASC;
