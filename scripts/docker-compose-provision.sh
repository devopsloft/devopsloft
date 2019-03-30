#!/usr/bin/env bash

set -e

export ENVIRONMENT=$1
export BASE_FOLDER=$2

cd $BASE_FOLDER

docker-compose up -d --build --force-recreate
