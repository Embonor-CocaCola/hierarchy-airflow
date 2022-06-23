import json
from datetime import datetime

import requests
from airflow.models import DAG
from airflow.operators.python import PythonOperator, ShortCircuitOperator

from base.utils.query_with_return import parameterized_query
from base.utils.slack import notify_start_task
from config.common.defaults import default_task_kwargs, default_dag_kwargs
from config.common.settings import airflow_root_dir
from config.reset_rejected_surveys.settings import RRS_DAG_ID, RRS_DAG_SCHEDULE_INTERVAL, RRS_DAG_START_DATE_VALUE


class ResetRejectedSurveysDagFactory:
    get_surveys_task_id = 'get_surveys_to_reject'
    reset_surveys_task_id = 'reset_surveys'

    @staticmethod
    def build() -> DAG:
        _start_date = datetime.strptime(
            RRS_DAG_START_DATE_VALUE, '%Y-%m-%d')
        _default_args = {
            **default_task_kwargs,
            'start_date': _start_date,
        }

        with DAG(
                RRS_DAG_ID,
                **default_dag_kwargs,
                schedule_interval=RRS_DAG_SCHEDULE_INTERVAL,
                default_args=_default_args,
                user_defined_filters={
                    'fromjson': lambda s: json.loads(s), 'replace_single_quotes': lambda s: s.replace("'", '"'),
                },
        ) as _dag:
            notify_rrs_dag_start = notify_start_task(_dag)

            get_surveys = ResetRejectedSurveysDagFactory.get_surveys_to_reset()

            check_obtained_surveys = ShortCircuitOperator(
                task_id='check_obtained_surveys',
                python_callable=lambda ti: ti.xcom_pull(task_ids=ResetRejectedSurveysDagFactory.get_surveys_task_id),
            )

            reset_surveys = PythonOperator(
                task_id=ResetRejectedSurveysDagFactory.reset_surveys_task_id,
                python_callable=ResetRejectedSurveysDagFactory.reset_surveys,
                execution_timeout=None,
                dag=_dag,
            )

            update_surveys = PythonOperator(
                task_id='update_resetted_surveys',
                python_callable=ResetRejectedSurveysDagFactory.update_surveys,
                dag=_dag,
            )

            notify_rrs_dag_start >> get_surveys >> check_obtained_surveys >> reset_surveys >> update_surveys

        return _dag

    @staticmethod
    def get_surveys_to_reset():
        with open(f'{airflow_root_dir}/include/sqls/reset_rejected_surveys/get_surveys_to_reset.sql', 'r') as file:
            sql = file.read()
            return PythonOperator(
                task_id=ResetRejectedSurveysDagFactory.get_surveys_task_id,
                python_callable=parameterized_query,
                op_args=[sql],
            )

    @staticmethod
    def reset_surveys(ti):
        to_reset = ti.xcom_pull(task_ids=ResetRejectedSurveysDagFactory.get_surveys_task_id)
        result = requests.post(
            'https://api.staging.embonorservices.cl/surveys-service/answers/reject',
            json=to_reset,
        )
        return result.json()

    @staticmethod
    def update_surveys(ti):
        to_reset = ti.xcom_pull(task_ids=ResetRejectedSurveysDagFactory.get_surveys_task_id)
        reset_response = ti.xcom_pull(task_ids=ResetRejectedSurveysDagFactory.reset_surveys_task_id)
        to_update = []
        errors = []

        for idx, response in enumerate(reset_response):
            if response['success']:
                to_update.append(to_reset[idx]['surveyId'])
            else:
                errors.append({'error': response['message'], 'details': to_reset[idx]})

        if errors:
            print('The following surveys could not be resetted:')
            for error in errors:
                print(error)

        if not to_update:
            return

        with open(f'{airflow_root_dir}/include/sqls/reset_rejected_surveys/update_reset_surveys.sql', 'r') as file:
            sql = file.read()
            parameterized_query(
                sql=sql, templates_dict={
                    'survey_source_ids': to_update,
                },
            )
