import json

import requests
from airflow.models import Variable

from expos_pdv.base.utils.query_with_return import parameterized_query
from expos_pdv.config.common.settings import SQL_PATH
from expos_pdv.config.maxerience_load.settings import ML_MAXERIENCE_BASE_URL


def close_complete_sessions():
    base_url = ML_MAXERIENCE_BASE_URL
    auth_token = Variable.get('ml_auth_token')

    with open(
            f'{SQL_PATH}/maxerience_load/get_completed_surveys_for_closing.sql', 'r',
    ) as file:
        sql = file.read()
    sessions = parameterized_query(sql, wrap=False)

    with open(f'{SQL_PATH}/maxerience_load/update_survey_analysis_completed.sql', 'r') as file:
        sql = file.read()

    for session in sessions:
        _, total_images, survey_id, session_start, visit_date, session_end = session
        print(f'Attempting to close session {session}')
        response = requests.post(
            f'{base_url}/uploadSessionSceneImages',
            files={
                'authToken': (None, auth_token),
                'data': (None, json.dumps({
                    'session': [
                        {
                            'sessionUid': str(survey_id),
                            'sessionStartTime': int(session_start),
                            'sessionEndTime': int(session_end),
                            'outletCode': '123321',
                            'visitDate': visit_date,
                            'scene': [],
                            'localTimeZone': 'CL',
                            'surveyStatus': 1,
                            'totalscene': int(total_images),
                            'totalSceneImages': int(total_images),
                        },
                    ],
                })),
            },
        )
        print('Response ready')
        json_response = response.json()
        print(json_response)

        if json_response['success']:
            print('updating survey_analysis')
            parameterized_query(sql, templates_dict={
                'survey_id': survey_id,
            })
