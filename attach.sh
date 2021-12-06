#!/bin/bash

container_id=`docker ps | awk '/airflow-worker_1/ {print $1}'`

docker exec -it $container_id /bin/bash
