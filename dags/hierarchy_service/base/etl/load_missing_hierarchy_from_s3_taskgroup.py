from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from hierarchy_service.base.utils.load_csv_into_temp_tables_taskgroup import LoadCsvIntoTempTablesTaskGroup
from hierarchy_service.base.utils.s3 import download_file_from_s3


class LoadMissingHierarchyFromS3TaskGroup:
    def __init__(self, dag: DAG, group_id: str) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.dag = dag
        self.group_id = group_id

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        download_task = PythonOperator(
            task_id='download_hierarchy_csv_from_s3',
            task_group=task_group,
            python_callable=download_file_from_s3,
            op_args=['missing_hierarchy', 'jerarquia'],
        )

        load_into_tmp_tables = LoadCsvIntoTempTablesTaskGroup(
            tables_to_insert=['missing_hierarchy'],
            task_group_id='load_missing_hierarchy_into_tmp_tables',
            sql_folder='etl',
            delimiter=',',
        ).build()

        download_task >> load_into_tmp_tables

        return task_group
