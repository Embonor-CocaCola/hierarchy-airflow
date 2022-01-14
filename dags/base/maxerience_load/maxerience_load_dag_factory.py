import json
import shutil
import uuid
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path

import requests
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from airflow.sensors.sql import SqlSensor

from base.maxerience_load.get_photos_to_upload_taskgroup import GetPhotosToUploadTaskGroup
from base.utils.build_maxerience_payload import build_maxerience_payload
from base.utils.ml_scene_info import extract_info_from_question_heading
from base.utils.query_with_return import parameterized_query
from config.expos_service.settings import airflow_root_dir, ES_STAGE
from config.maxerience_load.settings import ML_DAG_START_DATE_VALUE, ML_DAG_SCHEDULE_INTERVAL, ML_SQL_PATH, ML_DAG_ID, \
    ML_AIRFLOW_DATABASE_CONN_ID, ML_MAXERIENCE_BASE_URL, ML_MAXERIENCE_USER, ML_MAXERIENCE_PASS


class MaxerienceLoadDagFactory:
    def __init__(self):
        self._get_photos_group_id = 'get_photos_to_upload'
        self._get_questions_photos_id = 'get_questions_photos'

    def build(self) -> DAG:
        _start_date = datetime.strptime(
            ML_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(minutes=10),
            'retries': 2,
            'retry_delay': timedelta(seconds=5),
        }

        with DAG(
                ML_DAG_ID,
                schedule_interval=ML_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                template_searchpath=ML_SQL_PATH,
                max_active_runs=1,
                catchup=False,
                user_defined_filters={
                    'fromjson': lambda s: json.loads(s), 'replace_single_quotes': lambda s: s.replace("'", '"'),
                },
        ) as _dag:
            es_etl_finished_sensor = SqlSensor(
                task_id='es_etl_finished_sensor',
                conn_id=ML_AIRFLOW_DATABASE_CONN_ID,
                sql='maxerience_load/check_etl_status.sql',
                poke_interval=120,
                timeout=60 * 60 * 2,  # 2 hours
            )

            get_photos = GetPhotosToUploadTaskGroup(
                dag=_dag,
                group_id=self._get_photos_group_id,
                get_question_photos_id=self._get_questions_photos_id,
            ).build()

            download_photos = PythonOperator(
                task_id='download_photos',
                python_callable=self.download_photos,
                execution_timeout=None,
                dag=_dag,
            )

            load_photos_to_maxerience = PythonOperator(
                task_id='load_photos_to_maxerience',
                python_callable=self.load_photos_to_maxerience,
                execution_timeout=None,
                dag=_dag,
            )

            get_api_key = PythonOperator(
                task_id='get_api_key',
                python_callable=self.get_api_key,
                dag=_dag,
            )

            es_etl_finished_sensor >> get_api_key >> get_photos >> download_photos >> load_photos_to_maxerience

        return _dag

    def get_api_key(self):
        if ES_STAGE == 'production':
            response = requests.post(f'{ML_MAXERIENCE_BASE_URL}/login', files={
                'username': (None, ML_MAXERIENCE_USER),
                'password': (None, ML_MAXERIENCE_PASS),
            })
            json_response = response.json()
            if not json_response['success']:
                raise RuntimeError('Log in request failed. Could not get API KEY.')

            Variable.set('ml_auth_token', json_response['authToken'])

    def load_photos_to_maxerience(self, ti):
        photos_to_upload = ti.xcom_pull(task_ids=f'{self._get_photos_group_id}.{self._get_questions_photos_id}')
        base_path = Path(f'{airflow_root_dir}/data/ir_photos')
        print('Starting photo upload process...')

        auth_token = Variable.get('ml_auth_token')

        base_url = 'https://portal-stg1.maxerience.com/IrHandler'

        for survey in photos_to_upload:
            survey_id = survey[0]
            survey_created_at = survey[4]
            latitude = survey[2]
            longitude = survey[3]
            survey_answers = survey[1]
            print(f'Creating self_evaluation_analysis for survey: {survey_id}')

            analysis_id = self.create_self_evaluation_analysis(survey_id, survey_created_at)

            print(f'uploading photos of survey: {survey_id}')
            for answer in survey_answers:
                question_heading = answer['question']['heading']
                question_id = answer['question']['id']
                scene_info = extract_info_from_question_heading(question_heading)

                for photo_url in answer['attachments']:
                    scene_id = str(uuid.uuid4())
                    photo_name = photo_url.split('/')[-1]
                    with open(
                        base_path / survey_id / str(scene_info['scene']) / str(scene_info['sub_scene']) / photo_name,
                        'rb',
                    ) as file:
                        print(f'Sending request to maxerience for photo: {photo_name}')
                        r = requests.post(
                            f'{base_url}/uploadSessionSceneImages',
                            files=build_maxerience_payload(
                                img_file=file,
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
                        self.create_analyzed_photo(
                            analysis_id=analysis_id,
                            scene_info=scene_info,
                            scene_id=scene_id,
                            survey_id=survey_id,
                            question_id=question_id,
                            origin_url=photo_url,
                            sent_ok=json_response['success'],
                        )

    def download_photos(self, ti):
        try:
            shutil.rmtree(
                path='data/ir_photos',
                onerror=lambda a, b, c: print('WARN: Could not remove ir_photos folder. Maybe it did not exist.'),
            )
        except FileNotFoundError as error:
            print(error)

        path = Path(f'{airflow_root_dir}/data/ir_photos')  # ir = image recognition
        path.mkdir(parents=True, exist_ok=True)

        photos_to_download = ti.xcom_pull(task_ids=f'{self._get_photos_group_id}.{self._get_questions_photos_id}')

        for survey in photos_to_download:
            survey_id = survey[0]
            survey_answers = survey[1]
            print(f'Downloading photos of answer with id: {survey_id}')
            for answer in survey_answers:
                question_heading = answer['question']['heading']
                scene_info = extract_info_from_question_heading(question_heading)
                scene_path = Path(
                    f'{airflow_root_dir}/data/ir_photos/{survey_id}/{scene_info["scene"]}/{scene_info["sub_scene"]}')
                scene_path.mkdir(parents=True, exist_ok=True)
                print(f'Question heading: {question_heading}')
                for photo_url in answer['attachments']:
                    photo_name = photo_url.split('/')[-1]
                    urllib.request.urlretrieve(photo_url, scene_path / photo_name)

    def create_self_evaluation_analysis(self, survey_id, created_at):
        analysis_id = str(uuid.uuid4())

        with open(
                Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_load' / 'create_self_evaluation_analysis.sql',
                'r',
        ) as file:
            sql = file.read()
            parameterized_query(
                sql=sql,
                templates_dict={
                    'created_at': created_at,
                    'survey_id': survey_id,
                    'analysis_id': analysis_id,
                },
                is_procedure=True,
            )

        return analysis_id

    def create_analyzed_photo(self, analysis_id, scene_info, scene_id, survey_id, question_id, origin_url, sent_ok):
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
                    'analysis_id': analysis_id,
                    'scene_id': scene_id,
                    'question_id': question_id,
                    'origin_url': origin_url,
                    'sent_ok': sent_ok,
                },
            )
