#!/bin/bash

container_id=`docker ps | awk '/postgres/ {print $1}'`

(set -a && . .env; clean_conn_uri=${AIRFLOW__CORE__SQL_ALCHEMY_CONN/+psycopg2} ;docker exec -it $container_id psql $clean_conn_uri)
