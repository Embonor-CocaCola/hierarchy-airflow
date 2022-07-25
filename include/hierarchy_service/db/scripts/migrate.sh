#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

export PYTHONPATH="/opt/airflow/include/hierarchy_service/db"
# run migrations
python "${SCRIPT_PATH}/../manage.py" migrate
