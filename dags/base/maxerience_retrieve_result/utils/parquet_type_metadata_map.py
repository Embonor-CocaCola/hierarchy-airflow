from base.maxerience_retrieve_result.utils.product_row_to_db_record import product_row_to_db_record
from base.maxerience_retrieve_result.utils.recognized_product_row_to_record import recognized_product_row_to_record
from base.maxerience_retrieve_result.utils.scene_row_to_db_record import scene_row_to_db_record

parquet_type_metadata_map = {
    'product': {
        'row_to_record': product_row_to_db_record,
        'maxerience_name': 'IRProduct',
        'table_name': 'product',
        'columns': ['id::integer', 'identity::jsonb', 'display::jsonb', 'details::jsonb', 'recognition_details::jsonb',
                    'created_by_user_id::integer', 'created_on::timestamp',
                    'modified_by_user_id::integer', 'modified_on::timestamp',
                    'sku::integer', 'name::text', '"group"::text', 'category::text', 'local_category_name::text',
                    'is_foreign::boolean', 'flavour_name::text', 'manufacturer::text',
                    ],
    },
    'scene': {
        'row_to_record': scene_row_to_db_record,
        'maxerience_name': 'IRScenes',
        'table_name': 'analyzed_photo',
        'columns': ['id::uuid', 'verified_on::timestamp', 'source::text', 'image_quality::integer',
                    'created_on_time::timestamp', 'last_modified_time::timestamp',
                    'file_created_time::timestamp', 'external_id::integer', 'parquet_file_id::uuid'],
    },
    'recognized_product': {
        'row_to_record': recognized_product_row_to_record,
        'maxerience_name': 'IRActual',
        'table_name': 'recognized_product',
        'columns': ['id::uuid', 'analyzed_photo_id::uuid', 'product_id::integer', 'survey_id::uuid', 'position::jsonb',
                    'external_id::integer', 'block_id::text',
                    'door_index::integer', 'single_facings::integer', 'is_foreign::boolean', 're_id::text',
                    'file_created_time::timestamp'],
    },
}
