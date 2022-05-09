import uuid

import requests
from airflow import DAG
import xml.etree.ElementTree as ET

from pathlib import Path

from airflow.providers.postgres.operators.postgres import PostgresOperator
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json
from base.maxerience_retrieve_result.process_parquet_files_taskgroup import ProcessParquetFilesTaskGroup
from base.utils.query_with_return import multiple_insert_query
from base.utils.slack import build_status_msg, send_slack_notification
from config.common.settings import SHOULD_NOTIFY, airflow_root_dir
from config.expos_service.settings import ES_AIRFLOW_DATABASE_CONN_ID
from config.maxerience_retrieve_result.settings import (
    MRR_DAG_ID,
    MRR_DAG_SCHEDULE_INTERVAL,
    MRR_DAG_START_DATE_VALUE,
    MRR_SQL_PATH,
    MRR_SAS_KEY,
    MRR_REST_BASE_URL,
)
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


class MaxerienceRetrieveResultDagFactory:
    def __init__(self):
        self.rest_url = f'{MRR_REST_BASE_URL}embonor?{MRR_SAS_KEY}'
        register_adapter(dict, Json)

    @staticmethod
    def on_failure_callback(context):
        if not SHOULD_NOTIFY:
            return
        ti = context['task_instance']
        run_id = context['run_id']
        send_slack_notification(notification_type='alert',
                                payload=build_status_msg(
                                    dag_id=MRR_DAG_ID,
                                    status='failed',
                                    mappings={'run_id': run_id,
                                              'task_id': ti.task_id},
                                ))

    @staticmethod
    def on_success_callback(context):
        if not SHOULD_NOTIFY:
            return

        run_id = context['run_id']
        send_slack_notification(notification_type='success',
                                payload=build_status_msg(
                                    dag_id=MRR_DAG_ID,
                                    status='finished',
                                    mappings={'run_id': run_id},
                                ))

    def create_parquet_file(self, values):
        with open(
                Path(airflow_root_dir) / 'include' / 'sqls' / 'maxerience_retrieve_result' / 'create_parquet_file.sql',
                'r',
        ) as file:
            sql = file.read()
            multiple_insert_query(
                sql=sql,
                values=values,
            )

    def fetch_and_save_parquet_filenames(self):
        xml_data = requests.get(self.rest_url).content
        root = ET.fromstring(xml_data)
        insert_data = []

        for blob in root.findall('.//Blob'):
            url = blob.find('./Name').text
            created_at = blob.find('.//Creation-Time').text
            created_at_datetime = datetime.strptime(
                created_at, '%a, %d %b %Y %H:%M:%S %Z')  # ie: Wed, 19 Jan 2022 01:42:40 GMT
            content_type = url.split('/')[2]
            insert_data.append((str(uuid.uuid4()), created_at_datetime, content_type, url))

        self.create_parquet_file(insert_data)

    def build(self):
        _start_date = datetime.strptime(
            MRR_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(minutes=10),
            'retries': 0,
            'retry_delay': timedelta(seconds=5),
            'on_failure_callback': MaxerienceRetrieveResultDagFactory.on_failure_callback,
        }

        with DAG(
            MRR_DAG_ID,
            schedule_interval=MRR_DAG_SCHEDULE_INTERVAL,
            default_args=_default_args,
            template_searchpath=MRR_SQL_PATH,
            max_active_runs=1,
            catchup=False,
            on_success_callback=MaxerienceRetrieveResultDagFactory.on_success_callback,
        ) as _dag:

            if SHOULD_NOTIFY:
                notify_mrr_dag_start = PythonOperator(
                    task_id='notify_etl_start',
                    op_kwargs={
                        'payload': build_status_msg(
                            dag_id=MRR_DAG_ID,
                            status='started',
                            mappings={'run_id': '{{ run_id }}'},
                        ),
                        'notification_type': 'success'},
                    python_callable=send_slack_notification,
                    dag=_dag,
                )

            fetch_last_parquet_files = PythonOperator(
                task_id='fetch_last_parquet_files',
                python_callable=self.fetch_and_save_parquet_filenames,
            )

            process_parquet_files = ProcessParquetFilesTaskGroup(dag=_dag, group_id='process_parquet_files').build()

            preprocess_ir_data = PostgresOperator(
                task_id='preprocess_ir_data',
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                sql="""
                    REFRESH MATERIALIZED VIEW CONCURRENTLY preprocessed_success_photo;
                    REFRESH MATERIALIZED VIEW CONCURRENTLY preprocessed_essentials;
                    REFRESH MATERIALIZED VIEW CONCURRENTLY preprocessed_sovi;
                    REFRESH MATERIALIZED VIEW CONCURRENTLY preprocessed_edf;
                """,
            )

            if SHOULD_NOTIFY:
                notify_mrr_dag_start >> fetch_last_parquet_files

            fetch_last_parquet_files >> process_parquet_files >> preprocess_ir_data

        return _dag
