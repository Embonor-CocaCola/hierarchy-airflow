#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

# run migrations
python "${SCRIPT_PATH}/../manage.py" migrate --fake --database=expos
