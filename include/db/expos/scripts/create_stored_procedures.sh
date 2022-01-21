#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)
PROCEDURES_PATH="${SCRIPT_PATH}/../../../sqls/stored_procedures"

for file in $PROCEDURES_PATH/*; do
    echo "running ${file}..."
    python "${SCRIPT_PATH}/../manage.py" dbshell -- -f "${file}"
done
