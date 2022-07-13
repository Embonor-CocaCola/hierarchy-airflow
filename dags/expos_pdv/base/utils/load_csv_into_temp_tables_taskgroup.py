import os

from airflow.models import Variable

from expos_pdv.base.utils.additional_sql_params import additional_params
from expos_pdv.base.utils.table_names import TableNameManager
from airflow.utils.task_group import TaskGroup

from expos_pdv.base.utils.tasks import arrange_task_list_sequentially
from expos_pdv.config.etl.settings import ES_STAGE_TO_DOWNLOAD_CSVS_FROM_KEY
from expos_pdv.config.common.settings import STAGE, airflow_root_dir
from operators.postgres.copy_expert import PostgresOperatorCopyExpert
from operators.postgres.query_with_params import PostgresOperatorWithParams


class LoadCsvIntoTempTablesTaskGroup:
    def __init__(self, tables_to_insert: list[str], task_group_id: str, sql_folder,
                 pg_conn_id: str, delimiter=',', check_run=False):
        if not tables_to_insert:
            raise ValueError('missing parameter tables_to_insert')

        self.tables_to_insert = tables_to_insert
        self.task_group = TaskGroup(group_id=task_group_id)

        self.table_name_manager = TableNameManager(tables_to_insert)
        self.sql_folder = sql_folder
        self.delimiter = delimiter
        self.check_run = check_run
        self.csvs_stage = Variable.get(ES_STAGE_TO_DOWNLOAD_CSVS_FROM_KEY)
        self.pg_conn_id = pg_conn_id

    def create_insert_task(self, original_table_name: str):
        table_names = self.table_name_manager.get_variations(original_table_name)
        task_group = TaskGroup(group_id=f'insert_{table_names["tmp"]}')
        csv_path = os.path.join(airflow_root_dir, 'data', f'{original_table_name}.csv')
        params_key = self.create_params_key(original_table_name, check_run=self.check_run)

        create_temp_table_task = PostgresOperatorWithParams(
            postgres_conn_id=self.pg_conn_id,
            task_id=f'create_tmp_{table_names["normalized"]}',
            task_group=task_group,
            sql=os.path.join(
                self.sql_folder, table_names['normalized'], 'create_tmp_table.sql',
            ),
            parameters=additional_params.get(params_key, {}),
        )

        insert_tmp_task = PostgresOperatorCopyExpert(
            task_id=f'copy_into_{table_names["normalized"]}_from_csv',
            postgres_conn_id=self.pg_conn_id,
            task_group=task_group,
            table=f"airflow.{table_names['tmp']}",
            csv_path=csv_path,
            delimiter=self.delimiter,
        )

        create_temp_table_task >> insert_tmp_task

        return task_group

    def create_params_key(self, original_table_name, check_run: bool):
        return '.'.join([STAGE if check_run else self.csvs_stage, original_table_name, 'temp'])

    def build(self):
        with self.task_group as tg:
            arrange_task_list_sequentially(
                list(map(lambda table_name: self.create_insert_task(table_name), self.tables_to_insert)),
            )
            return tg
