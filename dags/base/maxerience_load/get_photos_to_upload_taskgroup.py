from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

import uuid

from base.utils.query_with_return import parameterized_query
from config.expos_service.settings import airflow_root_dir


class GetPhotosToUploadTaskGroup:
    def __init__(self, dag: DAG, group_id: str, get_question_photos_id: str) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.dag = dag
        self.group_id = group_id
        self.get_question_photos_id = get_question_photos_id

    def wrap_in_uuid(self, uuid_str_list):
        return tuple(map(lambda id: uuid.UUID(id), uuid_str_list))

    def get_question_photos(self, ti):
        q_ids = ti.xcom_pull(task_ids=f'{self.group_id}.get_question_ids')
        evaluation_ids = ti.xcom_pull(task_ids=f'{self.group_id}.get_non_analyzed_evaluations')
        with open(f'{airflow_root_dir}/include/sqls/maxerience_load/get_question_photos.sql', 'r') as file:
            sql = file.read()
        return parameterized_query(sql, wrap=False, templates_dict={
            'q_id': self.wrap_in_uuid(q_ids),
            'ev_id': self.wrap_in_uuid(evaluation_ids),
        })

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        with open(f'{airflow_root_dir}/include/sqls/maxerience_load/get_question_ids.sql', 'r') as file:
            sql = file.read()
            get_question_ids = PythonOperator(
                task_id='get_question_ids',
                task_group=task_group,
                python_callable=parameterized_query,
                op_args=[sql],
            )

        with open(f'{airflow_root_dir}/include/sqls/maxerience_load/get_non_analyzed_evaluations.sql', 'r') as file:
            sql = file.read()
            get_non_analyzed_evaluations = PythonOperator(
                task_id='get_non_analyzed_evaluations',
                task_group=task_group,
                python_callable=parameterized_query,
                op_args=[sql],
            )

        get_question_photos = PythonOperator(
            task_id=self.get_question_photos_id,
            task_group=task_group,
            python_callable=self.get_question_photos,
        )

        get_question_ids >> get_non_analyzed_evaluations >> get_question_photos
        return task_group
