#!/bin/bash

container_id=`docker ps | awk '/airflow\-service_postgres_1/ {print $1}'`

(set -a && . .env; clean_conn_uri=${AIRFLOW__CORE__SQL_ALCHEMY_CONN/+psycopg2} ;docker exec -it $container_id psql $clean_conn_uri)
