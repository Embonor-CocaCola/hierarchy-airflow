import json
from datetime import datetime, timedelta
from airflow.models import DAG
from airflow.sensors.sql import SqlSensor

from base.maxerience_load.get_photos_to_upload_taskgroup import GetPhotosToUploadTaskGroup
from config.maxerience_load.settings import ML_DAG_START_DATE_VALUE, ML_DAG_SCHEDULE_INTERVAL, ML_SQL_PATH, ML_DAG_ID, \
    ML_AIRFLOW_DATABASE_CONN_ID


class MaxerienceLoadDagFactory:
    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            ML_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            'owner': 'airflow',
            'start_date': _start_date,
            'provide_context': True,
            'execution_timeout': timedelta(minutes=10),
            'retries': 2,
            'retry_delay': timedelta(seconds=5),
        }

        with DAG(
                ML_DAG_ID,
                schedule_interval=ML_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                template_searchpath=ML_SQL_PATH,
                max_active_runs=1,
                catchup=False,
                user_defined_filters={
                    'fromjson': lambda s: json.loads(s), 'replace_single_quotes': lambda s: s.replace("'", '"'),
                },
        ) as _dag:
            es_etl_finished_sensor = SqlSensor(
                task_id='es_etl_finished_sensor',
                conn_id=ML_AIRFLOW_DATABASE_CONN_ID,
                sql='maxerience_load/check_etl_status.sql',
                poke_interval=120,
                timeout=60 * 60 * 2,  # 2 hours
            )

            get_photos = GetPhotosToUploadTaskGroup(dag=_dag, group_id='get_photos_to_upload').build()

            es_etl_finished_sensor >> get_photos
        return _dag
