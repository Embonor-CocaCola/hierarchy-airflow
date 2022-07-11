def scene_row_to_db_record(row, parquet_id):
    print(row)
    return (
        row['SceneUID'],
        row['VerifiedOn'],
        row['Source'],
        row['ImageQuality'],
        row['CreatedOnTime'],
        row['LastModifiedTime'],
        row['FileCreatedTime'],
        row['ID'],
        parquet_id,
    )
