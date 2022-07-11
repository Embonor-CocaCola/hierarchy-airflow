from pathlib import Path

import requests
from airflow.models import Variable

from expos_pdv.base.maxerience_load_retry.utils.update_analyzed_photo import update_analyzed_photo
from expos_pdv.base.utils.build_maxerience_payload import build_maxerience_payload
from expos_pdv.base.utils.ml_scene_info import extract_info_from_question_heading
from expos_pdv.base.utils.query_with_return import parameterized_query
from expos_pdv.config.common.settings import SQL_PATH
from expos_pdv.config.maxerience_load.settings import ML_MAXERIENCE_BASE_URL


def retry_uploads():
    with open(
            Path(SQL_PATH) / 'maxerience_load_retry' / 'get_pending_uploads.sql',
            'r',
    ) as file:
        sql = file.read()
    photos_to_download = parameterized_query(sql, wrap=False)
    print(f'Attempting to retry {len(photos_to_download)} photo uploads')
    base_url = ML_MAXERIENCE_BASE_URL
    auth_token = Variable.get('ml_auth_token')
    for photo in photos_to_download:
        print('Attempting retry of photo:')
        print(photo)
        photo_url = photo[2]
        survey_id = photo[0]
        scene_id = photo[1]
        latitude = photo[3]
        longitude = photo[4]
        survey_created_at = photo[5]
        question_heading = photo[6]

        scene_info = extract_info_from_question_heading(
            question_heading)

        photo_name = photo_url.split('/')[-1]
        print(f'Downloading photo: {photo_name}')

        photo_content = requests.get(photo_url).content
        print(
            f'Sending request to maxerience for photo: {photo_name}')

        r = requests.post(
            f'{base_url}/v2/uploadSessionSceneImages',
            files=build_maxerience_payload(
                img_file=photo_content,
                survey_id=survey_id,
                filename=photo_name,
                scene_info=scene_info,
                scene_id=scene_id,
                auth_token=auth_token,
                survey_created_at=survey_created_at.isoformat(),
                latitude=latitude,
                longitude=longitude,
            ),
        )
        print('Response ready')
        json_response = r.json()
        print(json_response)
        update_analyzed_photo(
            scene_id=scene_id,
            sent_ok=json_response['success'],
        )
