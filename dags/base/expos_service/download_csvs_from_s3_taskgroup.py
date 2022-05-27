from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from base.utils.s3 import download_file_from_s3
from base.utils.tasks import arrange_task_list_sequentially


class DownloadCsvsFromS3TaskGroup:
    def __init__(self, dag: DAG, group_id: str, file_names: list[str]) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.file_names = file_names
        self.dag = dag
        self.group_id = group_id

    def create_download_task(self, file_name: str, task_group: TaskGroup):
        return PythonOperator(
            task_id=f'download_{file_name}_csv_from_s3',
            task_group=task_group,
            python_callable=download_file_from_s3,
            op_args=[file_name, 'etl_csvs'],
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
