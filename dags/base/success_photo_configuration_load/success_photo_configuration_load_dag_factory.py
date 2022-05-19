from datetime import datetime, timedelta
import os
from airflow.models import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator

from base.utils.slack import build_status_msg, send_slack_notification
from base.utils.table_names import TableNameManager
from base.utils.tables_insert_taskgroup import TableOperationsTaskGroup
from base.utils.load_csv_into_temp_tables_taskgroup import LoadCsvIntoTempTablesTaskGroup
from base.success_photo_configuration_load.download_csv_task_group import DownloadCsvTaskGroup
from config.common.settings import SHOULD_NOTIFY
from config.expos_service.settings import ES_SQL_PATH, airflow_root_dir, ES_AIRFLOW_DATABASE_CONN_ID
from config.success_photo_configuration_load.settings import (
    SPCL_DAG_ID,
    SPCL_DAG_START_DATE_VALUE,
    SPCL_DAG_SCHEDULE_INTERVAL,
    SPCL_S3_CONN_ID,
    SPCL_TABLES_TO_EXTRACT,
)


class SuccessPhotoConfigurationLoadDagFactory:
    @ staticmethod
    def on_failure_callback(context):
        if not SHOULD_NOTIFY:
            return
        ti = context['task_instance']
        run_id = context['run_id']
        send_slack_notification(notification_type='alert',
                                payload=build_status_msg(
                                    dag_id=SPCL_DAG_ID,
                                    status='failed',
                                    mappings={'run_id': run_id,
                                              'task_id': ti.task_id},
                                ))

    @ staticmethod
    def on_success_callback(context):
        if not SHOULD_NOTIFY:
            return

        run_id = context['run_id']
        send_slack_notification(notification_type='success',
                                payload=build_status_msg(
                                    dag_id=SPCL_DAG_ID,
                                    status='finished',
                                    mappings={'run_id': run_id},
                                ))

    def __init__(self):
        pass

    def build(self) -> DAG:
        _start_date = datetime.strptime(
            SPCL_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(minutes=10),
            'retries': 1,
            'retry_delay': timedelta(seconds=15),
            'on_failure_callback': SuccessPhotoConfigurationLoadDagFactory.on_failure_callback,
        }
        _table_list = SPCL_TABLES_TO_EXTRACT
        _table_manager = TableNameManager(_table_list)
        _conform_operations = ['success_photo_product']
        _target_operations = _conform_operations
        _bucket_name = 'foto-de-exito'
        _config_name = SPCL_S3_CONN_ID
        _files_to_download = [{
            'original': 'dictionary',
            'address': 'diccionario_family_name/diccionario_FdE.csv',
            'file_name': 'Dictionary',
        }, {
            'original': 'success_photo_product',
            'address': 'foto_de_exito_cluster/Foto_de_Exito_NARTD.csv',
            'file_name': 'SuccessPhotoProduct',
        }]

        with DAG(
            SPCL_DAG_ID,
            schedule_interval=SPCL_DAG_SCHEDULE_INTERVAL,
            default_args=_default_args,
            template_searchpath=ES_SQL_PATH,
            max_active_runs=1,
            catchup=False,
            on_success_callback=SuccessPhotoConfigurationLoadDagFactory.on_success_callback,
        ) as dag:

            if SHOULD_NOTIFY:
                notify_etl_start = PythonOperator(
                    task_id='notify_etl_start',
                    op_kwargs={
                        'payload': build_status_msg(
                            dag_id=SPCL_DAG_ID,
                            status='started',
                            mappings={'run_id': '{{ run_id }}'},
                        ),
                        'notification_type': 'success'},
                    python_callable=send_slack_notification,
                    dag=dag,
                )

            download_csvs = DownloadCsvTaskGroup(
                bucket_name=_bucket_name,
                config_name=_config_name,
                download_folder=os.path.join(airflow_root_dir, 'data'),
                files_to_download=_files_to_download,
                task_group_id='download_csvs',
            ).build()

            load_into_tmp_tables = LoadCsvIntoTempTablesTaskGroup(
                tables_to_insert=_table_list,
                task_group_id='create_and_load_tmp_tables_from_csv',
                sql_folder='success_photo_configuration_load',
                delimiter=';',
            ).build()

            raw_tables_insert = TableOperationsTaskGroup(
                table_list=_table_manager.get_normalized_names(),
                sql_folder='success_photo_configuration_load',
                stage='raw',
            ).build()

            typed_tables_insert = TableOperationsTaskGroup(
                table_list=_table_manager.get_normalized_names(),
                sql_folder='success_photo_configuration_load',
                stage='typed',
            ).build()

            conform_tables_insert = TableOperationsTaskGroup(
                table_list=_conform_operations,
                sql_folder='success_photo_configuration_load',
                stage='conform',
            ).build()

            target_tables_insert = TableOperationsTaskGroup(
                table_list=_target_operations,
                sql_folder='success_photo_configuration_load',
                stage='target',
            ).build()

            update_and_refresh_data = PostgresOperator(
                task_id='update_and_refresh_data',
                postgres_conn_id=ES_AIRFLOW_DATABASE_CONN_ID,
                sql="""
                    REFRESH MATERIALIZED VIEW CONCURRENTLY sku_family_compliance;
                    CALL update_success_photo_products();
                """,
            )

            if SHOULD_NOTIFY:
                notify_etl_start >> download_csvs

            download_csvs >> load_into_tmp_tables >> raw_tables_insert >> typed_tables_insert
            typed_tables_insert >> conform_tables_insert >> target_tables_insert >> update_and_refresh_data

        return dag
