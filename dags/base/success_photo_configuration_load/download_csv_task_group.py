import os
from airflow.utils.task_group import TaskGroup
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

from config.common.settings import airflow_root_dir
from base.utils.tasks import arrange_task_list_sequentially


class DownloadCsvTaskGroup:
    def __init__(self, config_name: str, bucket_name: str, files_to_download: list[dict[str]],
                 task_group_id: str, download_folder: str):
        if not config_name:
            raise ValueError('missing parameter config_name')

        if not files_to_download:
            raise ValueError('missing parameter files_to_download')

        self.bucket_name = bucket_name
        self.config_name = config_name
        self.files_to_download = files_to_download
        self.task_group = TaskGroup(group_id=task_group_id)
        self.download_folder = download_folder
        self.task_group_id = task_group_id

    def create_download_task(self, file_to_download: dict[str]):
        task_group = TaskGroup(
            group_id=f"download_{file_to_download['original']}")

        download_from_s3 = PythonOperator(
            task_id=f"download_from_s3_{file_to_download['original']}",
            python_callable=self.download_from_s3,
            op_kwargs={
                'key': file_to_download['address'],
                'bucket_name': self.bucket_name,
                'local_path': os.path.join(airflow_root_dir, 'data'),
            },
            task_group=task_group,
        )

        rename_file = PythonOperator(
            task_id=f"rename_file_{file_to_download['original']}",
            python_callable=self.rename_file,
            op_kwargs={
                'file_to_download': file_to_download,
            },
            task_group=task_group,
        )

        download_from_s3 >> rename_file

        return task_group

    def download_from_s3(self, ti, key: str, bucket_name: str, local_path: str) -> str:
        hook = S3Hook(self.config_name)
        file_name = hook.download_file(
            key=key, bucket_name=bucket_name, local_path=local_path)
        return file_name

    def rename_file(self, ti, file_to_download: dict[str]) -> None:
        downloaded_file_name = ti.xcom_pull(
            task_ids=f"{self.task_group_id}.download_{file_to_download['original']}"
                     f".download_from_s3_{file_to_download['original']}")
        downloaded_file_path = '/'.join(
            downloaded_file_name.split('/')[:-1])
        os.rename(src=downloaded_file_name,
                  dst=f"{downloaded_file_path}/{file_to_download['file_name']}.csv")

    def build(self):
        with self.task_group as tg:
            arrange_task_list_sequentially(
                list(map(lambda file_to_download: self.create_download_task(
                    file_to_download), self.files_to_download)),
            )
            return tg
