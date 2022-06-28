from contextlib import ExitStack
from logging import info

from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup

from base.utils.mongo import execute_query, get_filters_per_docdb_collection
from base.utils.tasks import arrange_task_list_sequentially
from base.utils.tunneler import Tunneler
from config.common.settings import SHOULD_USE_TUNNEL
from config.expos_service.settings import (
    ES_EMBONOR_MONGO_CONN_ID,
    ES_EMBONOR_MONGO_DB_NAME,
)


class ExtractDocumentDbCsvTaskGroup:
    def __init__(self, dag: DAG, group_id: str, mongo_tunnel: Tunneler, collection_list: list) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')
        if SHOULD_USE_TUNNEL and not mongo_tunnel:
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
        filters = get_filters_per_docdb_collection(self.dag.dag_id).get(collection, None)
        return PythonOperator(
            task_id=f'extract_{collection}_to_csv',
            task_group=task_group,
            python_callable=self.extract_csv,
            op_args=[collection, filters],
        )

    def convert_fields_to_json(self, value):
        import json

        if type(value) in [list, dict]:
            return json.dumps(value, ensure_ascii=True)
        return value

    def extract_csv(self, collection_name: str, filters):
        import pandas
        from io import StringIO

        with self.mongo_tunnel if SHOULD_USE_TUNNEL else ExitStack():
            info(
                f'Starting extraction from document db collection: {collection_name}...')

            info('filters:')
            info(filters)
            jsondocs = execute_query(
                collection_name,
                ES_EMBONOR_MONGO_CONN_ID,
                ES_EMBONOR_MONGO_DB_NAME,
                tunnel=self.mongo_tunnel,
                filters=filters,
            )

            docs = pandas.read_json(StringIO(jsondocs))

            docs = docs.apply(lambda row: list(map(lambda field: self.convert_fields_to_json(field), row)))

            # Document databases do not guarantee order of fields so we need to order them manually for consistency
            docs.sort_index(axis=1, inplace=True)

            # noinspection PyTypeChecker
            docs.to_csv(f'/opt/airflow/data/{collection_name}.csv', index=False)

            info(f"Collection '{collection_name}' extracted successfully!")
