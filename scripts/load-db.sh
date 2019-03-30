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

timeout 60 bash -c \
  'while ! mysqladmin -h 127.0.0.1 ping --silent; do sleep 3; done'

mysqladmin -h 127.0.0.1 ping --silent
if [[ "$ENVIRONMENT" == "dev" ]]; then
  if [ -s $BASE_FOLDER/.dump.sql ]; then
    mysql -h 127.0.0.1 -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE <$BASE_FOLDER/.dump.sql
    if [ $? == 0 ]; then
      rm -rf $BASE_FOLDER/.dump.sql
    fi
  fi
else
  apt-get update
  apt-get install -y python3-pip
  pip3 install awscli
  exists=$(aws s3 ls s3://$AWS_BUCKET/.dump.sql)
  if [ -n "$exists" ]; then
    aws s3 cp s3://$AWS_BUCKET/.dump.sql .dump.sql
    mysql -h 127.0.0.1 -u root -p$MYSQL_ROOT_PASSWORD $MYSQL_DATABASE <.dump.sql
    if [ $? == 0 ]; then
      rm -rf .dump.sql
    fi
  fi
fi
