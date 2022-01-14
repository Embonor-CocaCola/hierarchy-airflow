#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

sh "${SCRIPT_PATH}/gac/scripts/migrate.sh"
sh "${SCRIPT_PATH}/gac/scripts/create_stored_procedures.sh"
