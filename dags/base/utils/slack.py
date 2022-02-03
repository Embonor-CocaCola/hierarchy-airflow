import json

import requests

import config.common.settings as config
from config.expos_service.settings import ES_STAGE, ES_ETL_DAG_ID
from config.maxerience_load.settings import ML_DAG_ID
webhooks_by_type = {
    'success': config.SLACK_SUCCESS_CHANNEL_URL,
    'alert': config.SLACK_FAILURE_CHANNEL_URL,
}

etl_sections_by_status = {
    'started': {
        'header': ':information_source: *EXPOS ETL* :postgresql:: Run started',
        'body': 'ETL with `run_id = %(run_id)s` has started',
    },
    'finished': {
        'header': ':white_check_mark: *EXPOS ETL* :postgresql:: Run finished',
        'body': 'ETL with `run_id = %(run_id)s` has finished successfully',
    },
    'failed': {
        'header': ':x: *EXPOS ETL* :postgresql:: Run failed',
        'body': 'ETL with `run_id = %(run_id)s` has failed at task with id `%(task_id)s`',
    },
}

ml_sections_by_status = {

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
