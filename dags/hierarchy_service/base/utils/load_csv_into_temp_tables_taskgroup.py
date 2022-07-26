import os

from hierarchy_service.base.utils.table_names import TableNameManager
from airflow.utils.task_group import TaskGroup

from hierarchy_service.base.utils.tasks import arrange_task_list_sequentially
from hierarchy_service.config.common.settings import airflow_root_dir, HIERARCHY_DATABASE_CONN_ID
from operators.postgres.copy_expert import PostgresOperatorCopyExpert
from operators.postgres.query_with_params import PostgresOperatorWithParams


class LoadCsvIntoTempTablesTaskGroup:
    def __init__(self, tables_to_insert: list[str], task_group_id: str, sql_folder, delimiter=',', check_run=False):
        if not tables_to_insert:
            raise ValueError('missing parameter tables_to_insert')

        self.tables_to_insert = tables_to_insert
        self.task_group = TaskGroup(group_id=task_group_id)

        self.table_name_manager = TableNameManager(tables_to_insert)
        self.sql_folder = sql_folder
        self.delimiter = delimiter
        self.check_run = check_run

    def create_insert_task(self, original_table_name: str):
        table_names = self.table_name_manager.get_variations(original_table_name)
        task_group = TaskGroup(group_id=f'insert_{table_names["tmp"]}')
        csv_path = os.path.join(airflow_root_dir, 'data', f'{original_table_name}.csv')

        create_temp_table_task = PostgresOperatorWithParams(
            postgres_conn_id=HIERARCHY_DATABASE_CONN_ID,
            task_id=f'create_tmp_{table_names["normalized"]}',
            task_group=task_group,
            sql=os.path.join(
                self.sql_folder, table_names['normalized'], 'create_tmp_table.sql',
            ),
        )

        insert_tmp_task = PostgresOperatorCopyExpert(
            task_id=f'copy_into_{table_names["normalized"]}_from_csv',
            postgres_conn_id=HIERARCHY_DATABASE_CONN_ID,
            task_group=task_group,
            table=f"airflow.{table_names['tmp']}",
            csv_path=csv_path,
            delimiter=self.delimiter,
        )

        create_temp_table_task >> insert_tmp_task

        return task_group

    def build(self):
        with self.task_group as tg:
            arrange_task_list_sequentially(
                list(map(lambda table_name: self.create_insert_task(table_name), self.tables_to_insert)),
            )
            return tg
