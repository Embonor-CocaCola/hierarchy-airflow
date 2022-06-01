from pathlib import Path

from base.utils.query_with_return import multiple_insert_query
from config.common.settings import airflow_root_dir


def create_parquet_file(values):
    with open(
            Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_retrieve_result' / 'create_parquet_file.sql',
            'r',
    ) as file:
        sql = file.read()
        multiple_insert_query(
            sql=sql,
            values=values,
        )
