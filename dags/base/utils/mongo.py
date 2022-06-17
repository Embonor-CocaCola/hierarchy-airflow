from contextlib import ExitStack

from airflow.providers.mongo.hooks.mongo import MongoHook
from bson import json_util

from config.expos_service.settings import IS_LOCAL_RUN, ES_STAGE


def execute_query(collection_name: str, conn_id: str, db_name: str, tunnel, filters=None):
    if filters is None:
        filters = {}

    with tunnel if IS_LOCAL_RUN else ExitStack():

        mongo_hook = MongoHook(
            mongo_conn_id=conn_id,
        )
        collection = mongo_hook.get_collection(
            mongo_collection=collection_name, mongo_db=db_name)
        cursor = collection.find(filter=filters)
        results = list(cursor)
        cursor.close()
        mongo_hook.close_conn()

    return json_dump_docs(results)


def get_filters_per_docdb_collection(dag_id):
    return {
        'answers': {
            'survey' if ES_STAGE != 'production' else 'surveyId': {
                '$in':
                    """{{ task_instance.xcom_pull(dag_id="%s", task_ids="%s") | from_json | object_ids_from_array }}"""
                    % (
                        dag_id,
                        'get_self_evaluation_survey_id',
                    ),
            },
        },
    }


def json_dump_docs(query_result):
    return json_util.dumps(
        query_result, ensure_ascii=True, json_options=json_util.JSONOptions(datetime_representation=2),
    )
