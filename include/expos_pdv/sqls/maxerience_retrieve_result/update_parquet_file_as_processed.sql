update parquet_file set processed_at = now() where id = %(parquet_file_id)s;
