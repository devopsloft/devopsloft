#!/usr/bin/env bash

# Usage: ./build/build.sh <environment>
# environment is one of [dev|ci|stage|prod]

source .env.$1
docker build --build-arg ENVIRONMENT=$ENVIRONMENT -t ${NAMESPACE}/spinner -f devopsloft/spinner/Dockerfile .
docker build -t ${NAMESPACE}/certbot --build-arg ENVIRONMENT=$1 -f devopsloft/certbot/Dockerfile .
docker-compose --env-file .env.$ENVIRONMENT -f docker-compose.yml build

if [ "$1" != "ci" ]; then
    docker push ${NAMESPACE}/certbot
    docker-compose --env-file .env.$ENVIRONMENT -f docker-compose.yml push
fi
