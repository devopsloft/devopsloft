#!/usr/bin/env bash

set -e

ENVIRONMENT=$1
BASE_FOLDER=$2

# shellcheck source=/dev/null
source $BASE_FOLDER/.env

if [[ "$ENVIRONMENT" == "stage" ]]; then
  AWS_BUCKET=$STAGE_AWS_BUCKET
elif [[ "$ENVIRONMENT" == "prod" ]]; then
  AWS_BUCKET=$PROD_AWS_BUCKET
fi

mysqladmin -h 127.0.0.1 ping --silent
if [ $? == 0 ]; then
  if [[ "$ENVIRONMENT" == "dev" ]]; then
    mysqldump -h 127.0.0.1 -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE >$BASE_FOLDER/.dump.sql
  else
    apt-get update
    apt-get install -y python3-pip
    pip3 install awscli
    mysqldump -h 127.0.0.1 -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE >.dump.sql
    if [ $? == 0 ]; then
      aws s3 cp .dump.sql s3://$AWS_BUCKET/.dump.sql
    fi
  fi
fi
