import os
from logging import info

from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from expos_pdv.config.success_photo_configuration_load.settings import SPCL_S3_CONN_ID
from hierarchy_service.config.common.settings import airflow_root_dir


def download_file_from_s3(file_name: str, folder_path: str):
    info(f'Starting download of csv: {file_name}.csv')

    s3_hook = S3Hook(
        SPCL_S3_CONN_ID,
    )

    file_key = f'{folder_path}/{file_name}.csv' if folder_path else f'{file_name}.csv'

    tmp_filename = s3_hook.download_file(
        key=file_key,
        bucket_name='expos-bucket',
        local_path=os.path.join(airflow_root_dir, 'data'),
    )

    os.rename(
        os.path.join(airflow_root_dir, 'data', tmp_filename),
        os.path.join(airflow_root_dir, 'data', f'{file_name}.csv'),
    )

    info('Download finished')
