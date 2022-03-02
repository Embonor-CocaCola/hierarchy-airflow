from base.maxerience_retrieve_result.utils.product_row_to_db_record import product_row_to_db_record
from base.maxerience_retrieve_result.utils.recognized_product_row_to_record import recognized_product_row_to_record
from base.maxerience_retrieve_result.utils.scene_row_to_db_record import scene_row_to_db_record

parquet_type_metadata_map = {
    'product': {
        'row_to_record': product_row_to_db_record,
        'maxerience_name': 'IRProduct',
        'table_name': 'product',
    },
    'scene': {
        'row_to_record': scene_row_to_db_record,
        'maxerience_name': 'IRScenes',
        'table_name': 'analyzed_photo',
    },
    'recognized_product': {
        'row_to_record': recognized_product_row_to_record,
        'maxerience_name': 'IRActual',
        'table_name': 'recognized_product',
    },
}
