import uuid
from psycopg2.extras import Json


def recognized_product_row_to_record(row, **kwargs):
    recognized_prod_id = uuid.uuid4()

    return (
        recognized_prod_id,
        uuid.UUID(row['SceneUID']),
        row['ProductID'],
        uuid.UUID(row['SessionUID']),
        Json({
            'shelf': row['Shelf'],
            'column': row['Position'],
            'stock_position': row['StockPos'],
            'orientation': row['OrientationId'],
        }),
        row['ID'],
        row['BlockID'],
        row['DoorIndex'],
        row['SingleFacings'],
        row['IsForeign'] or False,
        row['REId'],
        row['FileCreatedTime'],
    )
