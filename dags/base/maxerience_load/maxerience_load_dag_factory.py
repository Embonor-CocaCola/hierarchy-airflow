import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

import psycopg2
import requests
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator
from airflow.sensors.sql import SqlSensor

from base.maxerience_load.get_photos_to_upload_taskgroup import GetPhotosToUploadTaskGroup
from base.utils.build_maxerience_payload import build_maxerience_payload
from base.utils.ml_scene_info import extract_info_from_question_heading
from base.utils.query_with_return import parameterized_query
from base.utils.slack import send_slack_notification, build_status_msg
from config.common.settings import SHOULD_NOTIFY, EXPOS_DATABASE_CONN_ID
from config.expos_service.settings import airflow_root_dir, ES_STAGE
from config.maxerience_load.settings import (
    ML_DAG_START_DATE_VALUE,
    ML_DAG_SCHEDULE_INTERVAL,
    ML_SQL_PATH,
    ML_DAG_ID,
    ML_MAXERIENCE_BASE_URL,
    ML_MAXERIENCE_USER,
    ML_MAXERIENCE_PASS,
)


class MaxerienceLoadDagFactory:
    def __init__(self):
        self._get_photos_group_id = 'get_photos_to_upload'
        self._get_questions_photos_id = 'get_questions_photos'

    @staticmethod
    def on_failure_callback(context):
        if not SHOULD_NOTIFY:
            return
        ti = context['task_instance']
        run_id = context['run_id']
        send_slack_notification(notification_type='alert',
                                payload=build_status_msg(
                                    dag_id=ML_DAG_ID,
                                    status='failed',
                                    mappings={'run_id': run_id,
                                              'task_id': ti.task_id},
                                ))

    @staticmethod
    def on_success_callback(context):
        if not SHOULD_NOTIFY:
            return

        run_id = context['run_id']
        send_slack_notification(notification_type='success',
                                payload=build_status_msg(
                                    dag_id=ML_DAG_ID,
                                    status='finished',
                                    mappings={'run_id': run_id},
                                ))

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
            'on_failure_callback': MaxerienceLoadDagFactory.on_failure_callback,
        }

        with DAG(
                ML_DAG_ID,
                schedule_interval=ML_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                template_searchpath=ML_SQL_PATH,
                max_active_runs=1,
                catchup=False,
                on_success_callback=MaxerienceLoadDagFactory.on_success_callback,
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
            )

            if SHOULD_NOTIFY:
                notify_ml_dag_start = PythonOperator(
                    task_id='notify_etl_start',
                    op_kwargs={
                        'payload': build_status_msg(
                            dag_id=ML_DAG_ID,
                            status='started',
                            mappings={'run_id': '{{ run_id }}'},
                        ),
                        'notification_type': 'success'},
                    python_callable=send_slack_notification,
                    dag=_dag,
                )

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

            get_api_key = PythonOperator(
                task_id='get_api_key',
                python_callable=self.get_api_key,
                dag=_dag,
            )

            if SHOULD_NOTIFY:
                es_etl_finished_sensor >> notify_ml_dag_start >> get_api_key
            else:
                es_etl_finished_sensor >> get_api_key

            get_api_key >> get_photos >> download_and_upload_photos

        return _dag

    def get_api_key(self):
        if ES_STAGE == 'production':
            response = requests.post(f'{ML_MAXERIENCE_BASE_URL}/login', files={
                'username': (None, ML_MAXERIENCE_USER),
                'password': (None, ML_MAXERIENCE_PASS),
            })
            json_response = response.json()
            if not json_response['success']:
                raise RuntimeError(
                    'Log in request failed. Could not get API KEY.')

            Variable.set('ml_auth_token', json_response['authToken'])

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
                    self.create_analyzed_photo(
                        scene_info=scene_info,
                        scene_id=scene_id,
                        survey_id=survey_id,
                        question_id=question_id,
                        origin_url=photo_url,
                        sent_ok=json_response['success'],
                    )

            try:
                self.create_survey_analysis(
                    survey_id)
            except psycopg2.Error:
                pass

    def create_survey_analysis(self, survey_id):
        analysis_id = str(uuid.uuid4())

        with open(
                Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_load' / 'create_survey_analysis.sql',
                'r',
        ) as file:
            sql = file.read()
            parameterized_query(
                sql=sql,
                templates_dict={
                    'survey_id': survey_id,
                    'analysis_id': analysis_id,
                },
                is_procedure=True,
            )

        return analysis_id

    def create_analyzed_photo(self, scene_info, scene_id, survey_id, question_id, origin_url, sent_ok):
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
