#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

export PYTHONPATH="/opt/airflow/include/db/expos_pdv"
# run migrations
python "${SCRIPT_PATH}/../manage.py" migrate --database=expos
