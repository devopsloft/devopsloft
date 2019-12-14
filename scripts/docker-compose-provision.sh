#!/usr/bin/env bash

set -e

export ENVIRONMENT=$1
export BASE_FOLDER=$2
export WEB_HOST_PORT=$3
export WEB_GUEST_PORT=$4
export WEB_HOST_SECURE_PORT=$5
export WEB_GUEST_SECURE_PORT=$6
export HOMEPATH=$2

cd $BASE_FOLDER

docker-compose up -d --build --force-recreate
docker cp $BASE_FOLDER/vault/config/config.hcl vault:/vault/config
