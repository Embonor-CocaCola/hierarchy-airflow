import os
from logging import info

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.task_group import TaskGroup

from base.utils.tasks import arrange_task_list_sequentially
from config.common.settings import airflow_root_dir
from config.success_photo_configuration_load.settings import SPCL_S3_CONN_ID


class DownloadCsvsFromS3TaskGroup:
    def __init__(self, dag: DAG, group_id: str, file_names: list[str]) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.file_names = file_names
        self.dag = dag
        self.group_id = group_id

    def download_file(self, file_name: str):
        info(f'Starting download of csv: {file_name}.csv')

        s3_hook = S3Hook(
            SPCL_S3_CONN_ID,
        )

        s3_hook.download_file(
            key=f'etl_csvs/{file_name}',
            bucket_name='expos_bucket',
            local_path=os.path.join(airflow_root_dir, 'data', f'{file_name}.csv'),
        )
        info('Download finished')

    def create_download_task(self, file_name: str, task_group: TaskGroup):
        return PythonOperator(
            task_id=f'download_{file_name}_csv_from_s3',
            task_group=task_group,
            python_callable=self.download_file,
            op_args=[file_name],
        )

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        download_tasks = list(
            map(
                lambda file_name: self.create_download_task(file_name, task_group),
                self.file_names,
            ))

        arrange_task_list_sequentially(download_tasks)

        return task_group
