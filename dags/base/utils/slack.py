import json

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

import config.common.settings as config
from base.utils.conditional_operator import conditional_operator
from config.expos_service.settings import ES_STAGE, ES_ETL_DAG_ID, ES_ETL_CHECK_RUN_DAG_ID
from config.maintenance.settings import MTNC_DAG_ID
from config.maxerience_load.settings import ML_DAG_ID
from config.maxerience_load_retry.settings import MLR_DAG_ID
from config.maxerience_retrieve_result.settings import MRR_DAG_ID
from config.success_photo_configuration_load.settings import SPCL_DAG_ID

webhooks_by_type = {
    'success': config.SLACK_SUCCESS_CHANNEL_URL,
    'alert': config.SLACK_FAILURE_CHANNEL_URL,
}

details_by_dag = {
    ES_ETL_DAG_ID: {
        'emoji': ':postgresql:',
        'dag_name': 'EXPOS ETL',
    },
    ML_DAG_ID: {
        'emoji': ':camera:',
        'dag_name': 'MAXERIENCE LOAD DAG',
    },
    MRR_DAG_ID: {
        'emoji': ':open_file_folder:',
        'dag_name': 'MAXERIENCE RETRIEVE RESULT DAG',
    },
    MLR_DAG_ID: {
        'emoji': ':arrows_clockwise:',
        'dag_name': 'MAXERIENCE LOAD RETRY DAG',
    },
    SPCL_DAG_ID: {
        'emoji': ':selfie:',
        'dag_name': 'SUCCESS PHOTO CONFIGURATION LOAD',
    },
    ES_ETL_CHECK_RUN_DAG_ID: {
        'emoji': ':test_tube:',
        'dag_name': 'ETL CHECK RUN FOR STAGING',
    },
    MTNC_DAG_ID: {
        'emoji': ':screwdriver:',
        'dag_name': 'MAINTENANCE DAG',
    },
}


def get_sections_by_dag(dag_id):
    details = details_by_dag[dag_id]
    return {
        'started': {
            'header': f':information_source: *{details["dag_name"]}* {details["emoji"]}: Run started',
            'body': 'DAG with `run_id = %(run_id)s` has started',
        },
        'finished': {
            'header': f':white_check_mark: *{details["dag_name"]}* {details["emoji"]}: Run finished',
            'body': 'DAG with `run_id = %(run_id)s` has finished successfully',
        },
        'failed': {
            'header': f':x: *{details["dag_name"]}* {details["emoji"]}: Run failed',
            'body': 'DAG with `run_id = %(run_id)s` has failed at task with id `%(task_id)s`',
        },
    }


def build_status_msg(dag_id, status, mappings):
    return json.dumps({
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': get_sections_by_dag(dag_id)[status]['header'],
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': get_sections_by_dag(dag_id)[status]['body'] % mappings,
                },
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'Environment: *{ES_STAGE}*',
                    },
                ],
            },
        ],
    })


def send_slack_notification(notification_type, payload):
    webhook = webhooks_by_type[notification_type]
    requests.post(webhook, data=payload, headers={'content-type': 'application/json'})


def send_file_content_to_channels(file_content, channels, initial_comment, title):
    payload = {
        'content': file_content,
        'channels': ','.join(channels),
        'initial_comment': initial_comment,
        'title': title,
    }
    response = requests.post('https://slack.com/api/files.upload', data=payload, headers={
        'Authorization': f'Bearer {config.SLACK_EXPOS_BOT_TOKEN}',
    })
    print(response.json())


def on_failure_callback(context):
    if not config.SHOULD_NOTIFY:
        return
    ti = context['task_instance']
    run_id = context['run_id']
    dag_id = context['dag'].dag_id
    send_slack_notification(notification_type='alert',
                            payload=build_status_msg(
                                dag_id=dag_id,
                                status='failed',
                                mappings={'run_id': run_id, 'task_id': ti.task_id},
                            ))


def on_success_callback(context):
    if not config.SHOULD_NOTIFY:
        return
    run_id = context['run_id']
    dag_id = context['dag'].dag_id
    send_slack_notification(notification_type='success',
                            payload=build_status_msg(
                                dag_id=dag_id,
                                status='finished',
                                mappings={'run_id': run_id},
                            ))


def notify_start_task(dag: DAG):

    return conditional_operator(
        task_id='notify_etl_start',
        condition=config.SHOULD_NOTIFY,
        operator=PythonOperator,
        op_kwargs={
            'payload': build_status_msg(
                dag_id=dag.dag_id,
                status='started',
                mappings={'run_id': '{{ run_id }}'},
            ),
            'notification_type': 'success'},
        python_callable=send_slack_notification,
        dag=dag,
    )
