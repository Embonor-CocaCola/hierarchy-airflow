import os

import requests
from airflow.models.dag import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.task_group import TaskGroup
import io
import uuid
import pyarrow.parquet as pq

from base.maxerience_retrieve_result.utils.parquet_type_metadata_map import parquet_type_metadata_map
from base.utils.query_with_return import parameterized_query, copy_csv_to_table
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

        csv_path = f'{airflow_root_dir}/data/parquet_as_csv.csv'

        for parquet in unprocessed_parquets:
            parquet_filename = parquet[1]
            parquet_id = parquet[0]
            parquet_file_uri = f'{MRR_REST_BASE_URL}embonor/{parquet_filename}?{self.sas_key_for_download}'
            print(f'Attempting to download parquet file from {parquet_file_uri}')
            response = requests.get(parquet_file_uri)
            print('Obtained response! Converting to pyarrow table...')
            table_batches = pq.read_table(io.BytesIO(response.content)).to_batches(max_chunksize=100)

            if os.path.exists(csv_path):
                os.remove(csv_path)
                print('Previous csv file deleted successfully')
            else:
                print('There was no previous csv file')

            for batch in table_batches:

                print(f'Opening {csv_path} in append mode...')
                with open(csv_path, 'a') as file:
                    print('Opened file successfully. Attempting to iterate over pyarrow table...')
                    print('processing table batch...')
                    d = batch.to_pylist()
                    for row in d:
                        row_data = list(metadata['row_to_record'](row, parquet_id=parquet_id))
                        file.write(','.join(map(lambda value: f'|{str(value)}|', row_data)))
                        file.write('\n')

            print('Attempting to insert records...')
            copy_csv_to_table(table=metadata['table_name'], filepath=csv_path, columns=metadata['columns'])

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
