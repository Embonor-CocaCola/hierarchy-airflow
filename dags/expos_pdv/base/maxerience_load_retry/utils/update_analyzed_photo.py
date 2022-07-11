from pathlib import Path

from expos_pdv.base.utils.query_with_return import parameterized_query
from expos_pdv.config.common.settings import SQL_PATH


def update_analyzed_photo(scene_id, sent_ok):
    if not sent_ok:
        return

    with open(
            Path(SQL_PATH) / 'maxerience_load_retry' / 'update_analyzed_photo.sql',
            'r',
    ) as file:
        sql = file.read()
        parameterized_query(
            sql=sql,
            templates_dict={
                'scene_id': scene_id,
                'sent_ok': sent_ok,
            },
        )
