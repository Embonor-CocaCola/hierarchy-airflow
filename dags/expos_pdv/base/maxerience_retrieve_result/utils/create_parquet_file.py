from pathlib import Path

from expos_pdv.base.utils.query_with_return import multiple_insert_query
from expos_pdv.config.common.settings import SQL_PATH


def create_parquet_file(values):
    with open(
            Path(SQL_PATH) / 'maxerience_retrieve_result' / 'create_parquet_file.sql',
            'r',
    ) as file:
        sql = file.read()
        multiple_insert_query(
            sql=sql,
            values=values,
        )
