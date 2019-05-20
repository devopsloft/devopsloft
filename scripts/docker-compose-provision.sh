#!/usr/bin/env bash

set -ex

export ENVIRONMENT=$1
export BASE_FOLDER=$2

cd $BASE_FOLDER

docker-compose up -d --build --force-recreate
