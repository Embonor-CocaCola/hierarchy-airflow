import uuid

import requests
from airflow import DAG
import xml.etree.ElementTree as ET

from airflow.providers.postgres.operators.postgres import PostgresOperator
from psycopg2.extensions import register_adapter
from psycopg2.extras import Json

from expos_pdv.base.maxerience_retrieve_result.process_parquet_files_taskgroup import ProcessParquetFilesTaskGroup
from expos_pdv.base.maxerience_retrieve_result.refresh_mat_views_taskgroup import RefreshMatViewsTaskGroup
from expos_pdv.base.maxerience_retrieve_result.utils.create_parquet_file import create_parquet_file
from expos_pdv.base.utils.slack import notify_start_task
from expos_pdv.config.common.defaults import default_task_kwargs, default_dag_kwargs

from expos_pdv.config.etl.settings import ES_EXPOS_DATABASE_CONN_ID
from expos_pdv.config.maxerience_retrieve_result.settings import (
    MRR_DAG_ID,
    MRR_DAG_SCHEDULE_INTERVAL,
    MRR_DAG_START_DATE_VALUE,
    MRR_SAS_KEY,
    MRR_REST_BASE_URL,
)
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta


class MaxerienceRetrieveResultDagFactory:
    def __init__(self):
        self.rest_url = f'{MRR_REST_BASE_URL}embonor?{MRR_SAS_KEY}'
        register_adapter(dict, Json)

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
            insert_data.append(
                (str(uuid.uuid4()), created_at_datetime, content_type, url))

        create_parquet_file(insert_data)

    def build(self):
        _start_date = datetime.strptime(
            MRR_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
            'execution_timeout': timedelta(minutes=10),
        }

        with DAG(
            MRR_DAG_ID,
            **default_dag_kwargs,
            schedule_interval=MRR_DAG_SCHEDULE_INTERVAL,
            default_args=_default_args,
        ) as _dag:

            notify_mrr_dag_start = notify_start_task(_dag)

            fetch_last_parquet_files = PythonOperator(
                task_id='fetch_last_parquet_files',
                python_callable=self.fetch_and_save_parquet_filenames,
            )

            process_parquet_files = ProcessParquetFilesTaskGroup(
                dag=_dag, group_id='process_parquet_files').build()

            preprocess_ir_data = RefreshMatViewsTaskGroup(
                group_id='refresh_materialized_views',
                dag=_dag,
            ).build()

            preprocess_survey_metadata = PostgresOperator(
                task_id='preprocess_survey_metadata',
                postgres_conn_id=ES_EXPOS_DATABASE_CONN_ID,
                sql="""
                    CALL calculate_survey_metadata();
                """,
            )

            notify_mrr_dag_start >> fetch_last_parquet_files >> process_parquet_files >> preprocess_ir_data >> \
                preprocess_survey_metadata

        return _dag
