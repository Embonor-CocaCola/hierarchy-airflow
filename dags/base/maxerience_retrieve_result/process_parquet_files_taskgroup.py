import requests
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
import io
import uuid
import pyarrow.parquet as pq

from base.maxerience_retrieve_result.utils.parquet_type_metadata_map import parquet_type_metadata_map
from base.utils.query_with_return import parameterized_query, multiple_insert_query
from base.utils.tasks import arrange_task_list_sequentially
from config.expos_service.settings import airflow_root_dir
from config.maxerience_retrieve_result.settings import MRR_REST_BASE_URL, MRR_SAS_KEY


class ProcessParquetFilesTaskGroup:
    def __init__(self, dag: DAG, group_id: str) -> None:
        if not group_id:
            raise ValueError('group_id parameter is missing')
        if not dag:
            raise ValueError('dag parameter is missing')

        self.dag = dag
        self.group_id = group_id
        splitted_sas = MRR_SAS_KEY.split('&')[0:-2]
        self.sas_key_for_download = '&'.join(splitted_sas)
        self.parquet_types_to_process = ['product', 'scene', 'recognized_product']

    def wrap_in_uuid(self, uuid_str_list):
        return tuple(map(lambda id: uuid.UUID(id), uuid_str_list))

    def process_parquet_files(self, parquet_type):
        with open(
                f'{airflow_root_dir}/include/sqls/maxerience_retrieve_result/get_unprocessed_parquets.sql',
                'r',
        ) as file:
            sql = file.read()

        metadata = parquet_type_metadata_map[parquet_type]
        unprocessed_parquets = parameterized_query(sql, wrap=False, templates_dict={
            'content_type': metadata['maxerience_name'],
        })

        for parquet in unprocessed_parquets:
            parquet_filename = parquet[1]
            parquet_id = parquet[0]
            parquet_file_uri = f'{MRR_REST_BASE_URL}embonor/{parquet_filename}?{self.sas_key_for_download}'
            response = requests.get(parquet_file_uri)
            dataframe = pq.read_table(io.BytesIO(response.content)).to_pandas()

            insert_data = []

            for row in dataframe.to_dict(orient='records'):
                insert_data.append(metadata['row_to_record'](row, parquet_id=parquet_id))

            with open(
                    f'{airflow_root_dir}/include/sqls/maxerience_retrieve_result/{metadata["table_name"]}_inserts.sql',
                    'r',
            ) as file:
                sql = file.read()

            multiple_insert_query(sql, values=insert_data)

            with open(
                    f'{airflow_root_dir}/include/sqls/maxerience_retrieve_result/update_parquet_file_as_processed.sql',
                    'r',
            ) as file:
                sql = file.read()

            parameterized_query(sql, templates_dict={
                'parquet_file_id': parquet_id,
            })

            print(f'Entries from {parquet_filename} were inserted successfully')
        print(f'Processed all pending {metadata["table_name"]} parquet files')

    def build(self):
        task_group = TaskGroup(group_id=self.group_id)

        tasks = list(map(lambda content_type: PythonOperator(
            task_id=f'process_{content_type}_parquet_files',
            task_group=task_group,
            python_callable=self.process_parquet_files,
            execution_timeout=None,
            op_args=[content_type],
        ), self.parquet_types_to_process))

        arrange_task_list_sequentially(tasks)

        return task_group
