from pathlib import Path

from base.utils.query_with_return import parameterized_query
from config.common.settings import airflow_root_dir


def create_analyzed_photo(scene_info, scene_id, survey_id, question_id, origin_url, sent_ok):
    with open(
            Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_load' / 'create_analyzed_photo.sql',
            'r',
    ) as file:
        sql = file.read()
        parameterized_query(
            sql=sql,
            templates_dict={
                'scene_type': scene_info['scene'],
                'sub_scene_type': scene_info['sub_scene'],
                'survey_id': survey_id,
                'scene_id': scene_id,
                'question_id': question_id,
                'origin_url': origin_url,
                'sent_ok': sent_ok,
            },
        )
