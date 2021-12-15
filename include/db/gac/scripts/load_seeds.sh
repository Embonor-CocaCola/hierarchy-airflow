#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

# run seeds
python "${SCRIPT_PATH}/../manage.py" loaddata ${SCRIPT_PATH}/../seeds/*.json --database=expos
