import json
from datetime import datetime, timezone


def build_maxerience_payload(
        img_file,
        survey_id,
        filename,
        scene_info,
        scene_id,
        auth_token,
        survey_created_at,
        latitude,
        longitude,
):
    created_at = datetime.fromisoformat(survey_created_at)
    unix_timestamp = int(created_at.replace(tzinfo=timezone.utc).timestamp() * 1000)

    payload = {
        filename: (filename, img_file, 'application/jpeg'),
        'authToken': (None, auth_token),
        'data': {
            'session': [
                {
                    'sessionUid': survey_id,
                    'sessionStartTime': unix_timestamp,
                    'sessionEndTime': unix_timestamp + 3600 * 1000,  # One hour later
                    'outletCode': '123321',
                    'visitDate': created_at.date().isoformat(),
                    'localTimeZone': 'CL',
                    'latitude': latitude,
                    'longitude': longitude,
                    'attribute': {
                        'deviceName': None,
                        'deviceModel': None,
                        'osVersion': None,
                        'cameraManufacturer': None,
                        'cameraModel': None,
                        'cameraResolution': None,
                    },
                    'scene': [
                        {
                            'sceneUid': scene_id,
                            'sceneCaptureTime': unix_timestamp,
                            'sceneType': scene_info['scene'],
                            'sceneSubType': scene_info['sub_scene'],
                            'imageCount': 1,
                            'images': [
                                {
                                    'imageUid': scene_id,
                                    'imageCaptureTime': unix_timestamp,
                                    'imageUploadTime': unix_timestamp,
                                    'imageSerialNumber': 1,
                                    'imageGroupId': 1,
                                    'imageAttributes': {
                                        'cameraOrientation': 'Portrait',
                                        'screenRotationAuto': 'Off',
                                    },
                                    'imageFileName': filename,
                                },
                            ],
                        },
                    ],
                },
            ],
        },
    }

    payload['data'] = (None, json.dumps(payload['data']))
    return payload
