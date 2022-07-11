import json

import requests
from airflow import DAG
from airflow.operators.python import PythonOperator

import hierarchy_service.config.common.settings as config
from hierarchy_service.base.utils.conditional_operator import conditional_operator
from hierarchy_service.config.etl.settings import HIERARCHY_ETL_DAG_ID
from hierarchy_service.config.common.settings import STAGE, SLACK_CHANNEL_URL

details_by_dag = {
    HIERARCHY_ETL_DAG_ID: {
        'emoji': ':postgresql:',
        'dag_name': 'HIERARCHY ETL',
    },
}


sections = {
    'started': {
        'header': ':information_source: Run started',
        'body': 'DAG with `run_id = %(run_id)s` has started',
    },
    'finished': {
        'header': ':white_check_mark: Run finished',
        'body': 'DAG with `run_id = %(run_id)s` has finished successfully',
    },
    'failed': {
        'header': ':x: Run failed',
        'body': 'DAG with `run_id = %(run_id)s` has failed at task with id `%(task_id)s`',
    },
}


def build_status_msg(dag_id, status, mappings):
    details = details_by_dag[dag_id]
    return json.dumps({
        'username': details['dag_name'],
        'icon_emoji': details['emoji'],
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': sections[status]['header'],
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': sections[status]['body'] % mappings,
                },
            },
            {
                'type': 'context',
                'elements': [
                    {
                        'type': 'mrkdwn',
                        'text': f'Environment: *{STAGE}*',
                    },
                ],
            },
        ],
    })


def send_slack_notification(payload):
    webhook = SLACK_CHANNEL_URL
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
    send_slack_notification(payload=build_status_msg(dag_id=dag_id,
                                                     status='failed',
                                                     mappings={'run_id': run_id, 'task_id': ti.task_id},
                                                     ),
                            )


def on_success_callback(context):
    if not config.SHOULD_NOTIFY:
        return
    run_id = context['run_id']
    dag_id = context['dag'].dag_id
    send_slack_notification(payload=build_status_msg(dag_id=dag_id,
                                                     status='finished',
                                                     mappings={'run_id': run_id},
                                                     ),
                            )


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
