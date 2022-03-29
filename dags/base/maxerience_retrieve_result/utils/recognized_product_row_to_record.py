import json
import uuid


def recognized_product_row_to_record(row, **kwargs):
    recognized_prod_id = uuid.uuid4()

    return (
        recognized_prod_id,
        row['SceneUID'],
        row['ProductID'],
        row['SessionUID'],
        json.dumps({
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
        str(row['REId']),
        row['FileCreatedTime'],
    )
