import json
import os
from pathlib import Path
from datetime import timedelta
import shutil
import zipfile
import urllib.request
from functools import reduce
from airflow.models import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.models import Variable
import oci
from oci.object_storage import UploadManager
from oci.object_storage.transfer.constants import MEBIBYTE

from base.survey_monthly_photo_loader.health_checks_taskgroup import SmplHealthChecksTaskGroup
from base.utils.zip import zipdir
from config.expos_service.settings import (
    airflow_root_dir,
    SMPL_DAG_ID,
    ES_SQL_PATH,
    SMPL_DAG_START_DATE_VALUE,
    ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
    OCI_REGION,
    OCI_KEY,
    OCI_USER,
    OCI_TENANCY,
    OCI_FINGERPRINT,
)

oci_config = {
    'user': OCI_USER,
    'key_content': OCI_KEY,
    'fingerprint': OCI_FINGERPRINT,
    'tenancy': OCI_TENANCY,
    'region': OCI_REGION,
}

oci.config.validate_config(config=oci_config)
compartment_id = oci_config['tenancy']
object_storage = oci.object_storage.ObjectStorageClient(oci_config)


def progress_callback(bytes_uploaded):
    print('{} additional bytes uploaded'.format(bytes_uploaded))


class SmplDagFactory:
    def __init__(self):
        self.health_checks_instance = None

    def extract_data(self, ti):
        token = json.loads(
            ti.xcom_pull(task_ids=['smpl_health_checks.get_auth_token'])[0],
        )['token']
        return SimpleHttpOperator(
            task_id='get_answers_data',
            http_conn_id=ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
            endpoint=f'survey-service/answers/for-survey/{Variable.get("smpl_survey_id")}',
            method='GET',
            data={
                'from': Variable.get('mpl_from'),
                'to': Variable.get('smpl_to'),
            },
            headers={'Authorization': f'Bearer {token}'},
            do_xcom_push=True,
        )

    def transform_data(self, ti):
        data = json.loads(ti.xcom_pull(task_ids=['extract_data'])[0])
        questions_to_filter = Variable.get('smpl_questions').split('\r\n')
        processed = filter(
            bool,
            reduce(
                lambda prev, next: prev + next,
                map(
                    lambda atq: atq.get('attachments', []),
                    filter(
                        lambda atq: not Variable.get('smpl_questions') or atq.get('question') in questions_to_filter,
                        reduce(
                            lambda prev, next: prev + next,
                            map(
                                lambda answer: answer.get('answersToQuestions'),
                                data,
                            ),
                        ),
                    ),
                ),
            ),
        )
        return list(processed)

    def download(self, ti):
        try:
            shutil.rmtree(
                path='data/survey_photos',
                onerror=lambda a, b, c: print('WARN: Could not remove survey_photos folder. Maybe it did not exist.'),
            )
        except FileNotFoundError as error:
            print(error)

        path = Path(f'{airflow_root_dir}/data/survey_photos')
        path.mkdir(parents=True, exist_ok=True)

        urls = ti.xcom_pull(task_ids=['transform_data'])[0]
        for idx, url in enumerate(urls):
            photo_name = url.split('/')[-1]
            urllib.request.urlretrieve(url, f'data/survey_photos/{photo_name}')
            print(f'Downloaded photo N°{idx}')

    def compress(self, filename):
        with zipfile.ZipFile(f'{airflow_root_dir}/data/{filename}.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipdir(f'{airflow_root_dir}/data/survey_photos', zipf)

    def upload(self, file_name):
        file_path = f'{airflow_root_dir}/data/{file_name}'
        part_size = 2 * MEBIBYTE
        upload_manager = UploadManager(object_storage, allow_parallel_uploads=True, parallel_process_count=3)
        upload_manager.upload_file(
            'ax2bop5777vk',
            'survey-photos',
            file_name,
            file_path,
            part_size=part_size,
            progress_callback=progress_callback,
        )

        os.remove(file_path)

    def build(self) -> DAG:
        _default_args = {
            'owner': 'airflow',
            'provide_context': True,
            'execution_timeout': timedelta(seconds=60),
            'start_date': SMPL_DAG_START_DATE_VALUE,
            'retries': 0,
        }

        with DAG(
                SMPL_DAG_ID,
                schedule_interval=None,
                default_args=_default_args,
                template_searchpath=ES_SQL_PATH,
                max_active_runs=1,
                catchup=False,
                user_defined_filters={'fromjson': lambda s: json.loads(s)},
        ) as _dag:

            _folder_name = f'photos_{Variable.get("smpl_from")}_{Variable.get("smpl_to")}'
            _compressed_filename = f'{_folder_name}.zip'

            self.health_checks_instance = SmplHealthChecksTaskGroup(
                dag=_dag,
                group_id='smpl_health_checks',
            )

            extract_data = SimpleHttpOperator(
                task_id='extract_data',
                http_conn_id=ES_EMBONOR_SERVICES_BASE_URL_CONN_ID,
                endpoint=f'surveys-service/answers/for-survey/{Variable.get("smpl_survey_id")}',
                method='GET',
                data={
                    'from': Variable.get('smpl_from'),
                    'to': Variable.get('smpl_to'),
                },
                headers={'Authorization': "Bearer {{(ti.xcom_pull('smpl_health_checks.get_auth_token') | fromjson)["
                                          "'token']}}"},
                do_xcom_push=True,
            )

            transform_data = PythonOperator(
                task_id='transform_data',
                python_callable=self.transform_data,
                execution_timeout=None,
                do_xcom_push=True,
            )

            download_images = PythonOperator(
                task_id='download',
                python_callable=self.download,
                execution_timeout=None,
            )

            compress_images = PythonOperator(
                task_id='compress_images',
                python_callable=self.compress,
                op_args=[_folder_name],
                execution_timeout=None,
            )

            upload_compressed = PythonOperator(
                task_id='upload_compressed_images',
                python_callable=self.upload,
                op_args=[_compressed_filename],
                execution_timeout=None,
            )

            cleanup = BashOperator(
                task_id='cleanup',
                bash_command=f'cd {airflow_root_dir}/data && rm -rf survey_photos',
            )
            self.health_checks_instance.build() >> extract_data >> transform_data >> download_images >> compress_images
            compress_images >> upload_compressed >> cleanup
        return _dag
