import requests
from airflow.models import Variable

from config.maxerience_load.settings import ML_MAXERIENCE_BASE_URL, ML_MAXERIENCE_USER, ML_MAXERIENCE_PASS


def get_ir_api_key():
    response = requests.post(f'{ML_MAXERIENCE_BASE_URL}/login', files={
        'username': (None, ML_MAXERIENCE_USER),
        'password': (None, ML_MAXERIENCE_PASS),
    })
    json_response = response.json()
    if not json_response['success']:
        raise RuntimeError(
            'Log in request failed. Could not get API KEY.')

    Variable.set('ml_auth_token', json_response['authToken'])
