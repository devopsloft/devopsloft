#!/usr/bin/env bash

set -e

ENVIRONMENT=$1
HOME_DIR=$2
apt-get update
apt-get install -y mysql-client python3-pip docker-compose

ls $HOME_DIR/requirements.txt
pip3 install -r $HOME_DIR/requirements.txt

# shellcheck source=/vagrant/.env
source $HOME_DIR/.env
if [[ -f $HOME_DIR/.env.local ]]; then
# shellcheck source=/vagrant/.env.local
  source $HOME_DIR/.env.local
fi


export VAULT_GUEST_PORT=$VAULT_GUEST_PORT
export ENVIRONMENT=$ENVIRONMENT
if [[ $ENVIRONMENT == "stage" ]]; then
  AWS_S3_BUCKET=$STAGE_AWS_S3_BUCKET
elif [[ $ENVRIONEMT == "prod" ]]; then
  AWS_S3_BUCKET=$PROD_AWS_S3_BUCKET
else
  AWS_S3_BUCKET="undefined"
fi
export AWS_S3_BUCKET
mkdir -p $HOME_DIR/vault/config
chmod 777 $HOME_DIR/vault
j2 $HOME_DIR/vault/config.hcl.j2 -o $HOME_DIR/vault/config/config.hcl
