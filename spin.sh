#!/usr/bin/env bash

set -e



if [[ "$(uname)" != "Darwin" ]]; then
  echo "This script can run only on OS-X"
fi

ACTION=${1:-'up'}
ENVIRONMENT=${2:-'dev'}

function self_signed_certificate() {
    if [[ -f web_s2i/cert.pem && -f web_s2i/key.pem ]]; then
      return
    fi
    openssl req -x509 -newkey rsa:4096 -nodes -out web_s2i/cert.pem \
      -keyout web_s2i/key.pem -days 365 \
      -subj "/C=IL/ST=Gush-Dan/L=Tel-Aviv/O=DevOps Loft/OU=''/CN=''"
}

self_signed_certificate

source .env

if [[ "$ENVIRONMENT" == "dev" ]]; then
  if [[ $(vboxmanage --version) != "6.0.8r130520" ]]; then
    echo "Wrong virtualbox version"
  fi

  vagrant box update --provider virtualbox
  vagrant box prune  --provider virtualbox

  export WEB_HOST_PORT=$DEV_WEB_HOST_PORT
  export WEB_GUEST_PORT=$DEV_WEB_GUEST_PORT
  export WEB_HOST_SECURE_PORT=$DEV_WEB_HOST_SECURE_PORT
  export WEB_GUEST_SECURE_PORT=$DEV_WEB_GUEST_SECURE_PORT
elif [[ "$ENVIRONMENT" == "stage" ]]; then
  export AWS_PROFILE=$STAGE_AWS_PROFILE
  export WEB_HOST_PORT=$STAGE_WEB_HOST_PORT
  export WEB_GUEST_PORT=$STAGE_WEB_GUEST_PORT
  export WEB_HOST_SECURE_PORT=$STAGE_WEB_HOST_SECURE_PORT
  export WEB_GUEST_SECURE_PORT=$STAGE_WEB_GUEST_SECURE_PORT
  if [[ -f record-set-create.json ]]; then
    source venv/bin/activate
    pip install --upgrade awscli
    sed 's/CREATE/DELETE/g' record-set-create.json >record-set-delete.json
    aws route53 change-resource-record-sets \
      --hosted-zone-id $STAGE_HOSTED_ZONE_ID \
      --change-batch file://record-set-delete.json
    rm -rf record-set-create.json record-set-delete.json
  fi
elif [[ "$ENVIRONMENT" == "prod" ]]; then
  export AWS_PROFILE=$PROD_AWS_PROFILE
  export WEB_HOST_PORT=$PROD_WEB_HOST_PORT
  export WEB_GUEST_PORT=$PROD_WEB_GUEST_PORT
  export WEB_HOST_SECURE_PORT=$PROD_WEB_HOST_SECURE_PORT
  export WEB_GUEST_SECURE_PORT=$PROD_WEB_GUEST_SECURE_PORT
fi

vagrant destroy -f $ENVIRONMENT
if [[ "$ACTION" == "destroy" ]]; then
  exit
fi
vagrant up $ENVIRONMENT
guest_ip=$(vagrant ssh-config $ENVIRONMENT | grep HostName | awk \{'print $2'\})

if [[ "$ENVIRONMENT" == "dev" ]]; then
  sleep 5
elif [[ "$ENVIRONMENT" == "stage" ]]; then
  source venv/bin/activate
  pip install --upgrade awscli j2cli
  export domain_name=www.dpline.io
  export guest_ip
  j2 record-set.json.j2 -o record-set-create.json
  aws route53 change-resource-record-sets \
    --hosted-zone-id $STAGE_HOSTED_ZONE_ID \
    --change-batch file://record-set-create.json
fi

"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --disable-application-cache "https://${guest_ip}:${WEB_HOST_SECURE_PORT}"
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --disable-application-cache "http://${guest_ip}:$WEB_HOST_PORT"
