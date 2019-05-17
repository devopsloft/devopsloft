#!/usr/bin/env bash

set -ex

export ENVIRONMENT=$1
export BASE_FOLDER=$2

mkdir .devopsloft

cd $BASE_FOLDER

docker-compose up -d --build --force-recreate
docker-compose exec -dT vault_cli vault-init.py
