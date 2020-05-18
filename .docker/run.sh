#!/usr/bin/env bash

MYSQL_SRC_DIR=${1:-`pwd`/../sql}
MYSQL_ROOT_PASSWORD=${MYSQL_ROOT_PASSWORD:-'password'}

docker run \
    --name property-scraper-mysql \
    --publish 3306:3306 \
    --publish 33060:33060 \
    --volume $MYSQL_SRC_DIR:/docker-entrypoint-initdb.d \
    --env MYSQL_ROOT_PASSWORD=$MYSQL_ROOT_PASSWORD \
    --detach \
    mysql:latest
