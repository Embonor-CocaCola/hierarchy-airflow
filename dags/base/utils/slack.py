import json

import requests

import config.common.settings as config
from config.expos_service.settings import ES_STAGE

webhooks_by_type = {
    'success': config.SLACK_SUCCESS_CHANNEL_URL,
    'alert': config.SLACK_FAILURE_CHANNEL_URL,
}

etl_sections_by_status = {
    'started': {
        'header': ':information_source: *EXPOS ETL*: Run started',
        'body': 'ETL with `run_id = %(run_id)s` has started',
    },
    'finished': {
        'header': ':white_check_mark: *EXPOS ETL*: Run finished',
        'body': 'ETL with `run_id = %(run_id)s` has finished successfully',
    },
    'failed': {
        'header': ':x: *EXPOS ETL*: Run failed',
        'body': 'ETL with `run_id = %(run_id)s` has failed at task with id `%(task_id)s`',
    },
}


def build_etl_status_msg(status, mappings):
    return json.dumps({
        'blocks': [
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': etl_sections_by_status[status]['header'],
                },
            },
            {
                'type': 'section',
                'text': {
                    'type': 'mrkdwn',
                    'text': etl_sections_by_status[status]['body'] % mappings,
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
