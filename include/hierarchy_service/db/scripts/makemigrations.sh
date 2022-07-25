#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

# make migrations
python "${SCRIPT_PATH}/../manage.py" makemigrations $1
