#!/usr/bin/env sh

SCRIPT_PATH=$(dirname $0)

# run migrations and seeds for gac
sh "${SCRIPT_PATH}/gac/scripts/migrate.sh"
# sh "${SCRIPT_PATH}/gac/scripts/load_seeds.sh"
