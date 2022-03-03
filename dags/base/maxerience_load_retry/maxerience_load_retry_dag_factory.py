import json
from datetime import datetime, timedelta
from pathlib import Path

import requests
from airflow.models import DAG, Variable
from airflow.operators.python import PythonOperator

from base.utils.build_maxerience_payload import build_maxerience_payload
from base.utils.ml_scene_info import extract_info_from_question_heading
from base.utils.query_with_return import parameterized_query
from base.utils.slack import send_slack_notification, build_status_msg
from config.common.settings import SHOULD_NOTIFY
from config.expos_service.settings import airflow_root_dir, ES_STAGE
from config.maxerience_load.settings import (
    ML_MAXERIENCE_BASE_URL,
    ML_MAXERIENCE_USER,
    ML_MAXERIENCE_PASS,
)
from config.maxerience_load_retry.settings import (
    MLR_SQL_PATH,
    MLR_DAG_ID,
    MLR_DAG_SCHEDULE_INTERVAL,
    MLR_DAG_START_DATE_VALUE,
)


class MaxerienceLoadRetryDagFactory:
    @staticmethod
    def on_failure_callback(context):
        if not SHOULD_NOTIFY:
            return
        ti = context['task_instance']
        run_id = context['run_id']
        send_slack_notification(notification_type='alert',
                                payload=build_status_msg(
                                    dag_id=MLR_DAG_ID,
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
                                    dag_id=MLR_DAG_ID,
                                    status='finished',
                                    mappings={'run_id': run_id},
                                ))

    def __init__(self):
        pass

    def build(self) -> DAG:
        _start_date = datetime.strptime(
            MLR_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(minutes=10),
            'retries': 1,
            'retry_delay': timedelta(seconds=15),
            'on_failure_callback': MaxerienceLoadRetryDagFactory.on_failure_callback,
        }

        with DAG(
                MLR_DAG_ID,
                schedule_interval=MLR_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                template_searchpath=MLR_SQL_PATH,
                max_active_runs=1,
                catchup=False,
                on_success_callback=MaxerienceLoadRetryDagFactory.on_success_callback,
                user_defined_filters={
                    'fromjson': lambda s: json.loads(s), 'replace_single_quotes': lambda s: s.replace("'", '"'),
                },
        ) as _dag:

            if SHOULD_NOTIFY:
                notify_ml_dag_start = PythonOperator(
                    task_id='notify_dag_start',
                    op_kwargs={
                        'payload': build_status_msg(
                            dag_id=MLR_DAG_ID,
                            status='started',
                            mappings={'run_id': '{{ run_id }}'},
                        ),
                        'notification_type': 'success'},
                    python_callable=send_slack_notification,
                    dag=_dag,
                )

            get_api_key = PythonOperator(
                task_id='get_api_key',
                python_callable=self.get_api_key,
                dag=_dag,
            )

            retry_uploads = PythonOperator(
                task_id='retry_uploads',
                python_callable=self.retry_uploads,
                execution_timeout=None,
            )

            if SHOULD_NOTIFY:
                notify_ml_dag_start >> get_api_key

            get_api_key >> retry_uploads

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

    def retry_uploads(self):
        with open(
                Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_load_retry' / 'get_pending_uploads.sql',
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
                    survey_created_at=survey_created_at,
                    latitude=latitude,
                    longitude=longitude,
                ),
            )
            print('Response ready')
            json_response = r.json()
            print(json_response)
            self.update_analyzed_photo(
                scene_id=scene_id,
                sent_ok=json_response['success'],
            )

    def update_analyzed_photo(self, scene_id, sent_ok):
        if not sent_ok:
            return

        with open(
                Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_load_retry' / 'update_analyzed_photo.sql',
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
