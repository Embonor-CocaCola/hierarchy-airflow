import json
from io import StringIO
from contextlib import ExitStack
from logging import info

import pandas
from bson import json_util
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.mongo.hooks.mongo import MongoHook
from airflow.utils.task_group import TaskGroup

from base.utils.tasks import arrange_task_list_sequentially
from base.utils.tunneler import Tunneler
from config.expos_service.settings import (
    ES_EMBONOR_MONGO_CONN_ID,
    ES_EMBONOR_MONGO_DB_NAME,
    IS_LOCAL_RUN,
)


class ExtractMongoCsvTaskGroup:
    def __init__(self, dag: DAG, group_id: str, mongo_tunnel: Tunneler, collection_list: list) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')
        if IS_LOCAL_RUN and not mongo_tunnel:
            raise ValueError('mongo_tunnel must be supplied for local runs')

        self.dag = dag
        self.group_id = group_id
        self.collection_list = collection_list
        self.mongo_tunnel = mongo_tunnel

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        extract_tasks = list(map(lambda collection: self.create_extract_task(
            collection, task_group), self.collection_list))

        arrange_task_list_sequentially(extract_tasks)

        return task_group

    def create_extract_task(self, collection, task_group):
        return PythonOperator(
            task_id=f'extract_{collection}_to_csv',
            task_group=task_group,
            python_callable=self.extract_csv,
            op_args=[collection],
        )

    def convert_fields_to_json(self, value):
        if type(value) in [list, dict]:
            return json.dumps(value, ensure_ascii=False)
        return value

    def extract_csv(self, collection_name: str):
        with self.mongo_tunnel if IS_LOCAL_RUN else ExitStack():
            info(
                f'Starting extraction from mongo collection: {collection_name}...')

            mongo_hook = MongoHook(
                mongo_conn_id=ES_EMBONOR_MONGO_CONN_ID,
            )
            collection = mongo_hook.get_collection(
                mongo_collection=collection_name, mongo_db=ES_EMBONOR_MONGO_DB_NAME)
            cursor = collection.find()

            jsondocs = json.dumps(list(cursor), default=json_util.default, ensure_ascii=False)
            docs = pandas.read_json(StringIO(jsondocs))

            docs = docs.apply(lambda row: list(map(lambda field: self.convert_fields_to_json(field), row)))

            # noinspection PyTypeChecker
            docs.to_csv(f'/opt/airflow/include/data/{collection_name}.csv', index=False)

            info(f"Collection '{collection_name}' extracted successfully!")
