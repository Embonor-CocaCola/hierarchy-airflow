import json
import uuid
from datetime import datetime

import psycopg2
import requests
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from airflow.sensors.sql import SqlSensor

from base.maxerience_load.get_photos_to_upload_taskgroup import GetPhotosToUploadTaskGroup
from base.maxerience_load.utils.close_complete_sessions import close_complete_sessions
from base.maxerience_load.utils.create_analyzed_photo import create_analyzed_photo
from base.maxerience_load.utils.create_survey_analysis import create_survey_analysis
from base.maxerience_load.utils.get_ir_api_key import get_ir_api_key
from base.utils.build_maxerience_payload import build_maxerience_payload
from base.utils.conditional_operator import conditional_operator
from base.utils.ml_scene_info import extract_info_from_question_heading
from base.utils.slack import notify_start_task
from config.common.defaults import default_task_kwargs, default_dag_kwargs
from config.common.settings import EXPOS_DATABASE_CONN_ID, STAGE
from config.maxerience_load.settings import (
    ML_DAG_START_DATE_VALUE,
    ML_DAG_SCHEDULE_INTERVAL,
    ML_DAG_ID,
    ML_MAXERIENCE_BASE_URL,
)


class MaxerienceLoadDagFactory:
    def __init__(self):
        self._get_photos_group_id = 'get_photos_to_upload'
        self._get_questions_photos_id = 'get_questions_photos'

    def build(self) -> DAG:
        _start_date = datetime.strptime(
            ML_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
        }

        with DAG(
                ML_DAG_ID,
                **default_dag_kwargs,
                schedule_interval=ML_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                user_defined_filters={
                    'fromjson': lambda s: json.loads(s), 'replace_single_quotes': lambda s: s.replace("'", '"'),
                },
        ) as _dag:

            es_etl_finished_sensor = SqlSensor(
                task_id='es_etl_finished_sensor',
                conn_id=EXPOS_DATABASE_CONN_ID,
                sql='maxerience_load/check_etl_status.sql',
                poke_interval=120,
                timeout=60 * 60 * 2,  # 2 hours
                execution_timeout=None,
            )

            notify_ml_dag_start = notify_start_task(_dag)

            get_photos = GetPhotosToUploadTaskGroup(
                dag=_dag,
                group_id=self._get_photos_group_id,
                get_question_photos_id=self._get_questions_photos_id,
            ).build()

            download_and_upload_photos = PythonOperator(
                task_id='download_and_upload_photos',
                python_callable=self.download_and_upload_photos,
                execution_timeout=None,
                dag=_dag,
            )

            get_api_key = conditional_operator(
                task_id='get_api_key',
                operator=PythonOperator,
                condition=STAGE == 'production',
                python_callable=get_ir_api_key,
                dag=_dag,
            )

            close_complete_sessions_task = PythonOperator(
                task_id='close_complete_sessions',
                python_callable=close_complete_sessions,
                execution_timeout=None,
                dag=_dag,
            )

            es_etl_finished_sensor >> notify_ml_dag_start >> get_api_key >> get_photos >> download_and_upload_photos >>\
                close_complete_sessions_task

        return _dag

    def download_and_upload_photos(self, ti):
        photos_to_download = ti.xcom_pull(
            task_ids=f'{self._get_photos_group_id}.{self._get_questions_photos_id}')
        base_url = ML_MAXERIENCE_BASE_URL
        auth_token = Variable.get('ml_auth_token')

        for survey in photos_to_download:
            survey_id = survey[0]
            survey_answers = survey[1]
            latitude = survey[2]
            longitude = survey[3]
            survey_created_at = survey[4]

            print(
                f'Downloading and uploading photos of answer with id: {survey_id}')
            for answer in survey_answers:
                question_heading = answer['question']['heading']
                scene_info = extract_info_from_question_heading(
                    question_heading)
                question_id = answer['question']['id']

                print(f'Question heading: {question_heading}')
                for photo_url in answer['attachments']:
                    scene_id = str(uuid.uuid4())

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
                            survey_created_at=survey_created_at,
                            latitude=latitude,
                            longitude=longitude,
                        ),
                    )
                    print('Response ready')
                    json_response = r.json()
                    print(json_response)
                    create_analyzed_photo(
                        scene_info=scene_info,
                        scene_id=scene_id,
                        survey_id=survey_id,
                        question_id=question_id,
                        origin_url=photo_url,
                        sent_ok=json_response['success'],
                    )

            try:
                create_survey_analysis(
                    survey_id)
            except psycopg2.Error:
                pass
