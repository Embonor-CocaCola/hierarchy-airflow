import os
from logging import info

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.utils.task_group import TaskGroup

from hierarchy_service.base.utils.tasks import arrange_task_list_sequentially
from hierarchy_service.config.common.settings import EXPOS_S3_CONN_ID, airflow_root_dir, STAGE


class UploadCsvsToS3TaskGroup:
    def __init__(self, dag: DAG, group_id: str, file_names: list[str]) -> None:
        if not group_id:
            raise ValueError("group_id parameter is missing")
        if not dag:
            raise ValueError("dag parameter is missing")

        self.file_names = file_names
        self.dag = dag
        self.group_id = group_id

    def upload_file(self, file_name: str):
        info(f"Starting upload of csv: {file_name}.csv")

        s3_hook = S3Hook(
            EXPOS_S3_CONN_ID,
        )
        s3_hook.load_file(
            filename=os.path.join(airflow_root_dir, "data", f"{file_name}.csv"),
            key=f"hierarchy_tables/{STAGE}/{file_name}.csv",
            bucket_name="expos-bucket",
            replace=True,
        )
        info("upload finished")

    def create_upload_task(self, file_name: str, task_group: TaskGroup):
        return PythonOperator(
            task_id=f"upload_{file_name}_csv_to_s3",
            task_group=task_group,
            python_callable=self.upload_file,
            op_args=[file_name],
        )

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        upload_tasks = [self.create_upload_task(file_name, task_group) for file_name in self.file_names]

        arrange_task_list_sequentially(upload_tasks)

        return task_group
