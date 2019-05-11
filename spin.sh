#!/usr/bin/env bash

set -e

if [[ "$(uname)" != "Darwin" ]]; then
  echo "This script can run only on OS-X"
fi

env=${1:-'dev'}

if [[ "$env" == "dev" ]]; then
  vagrant box update --provider virtualbox
  port=5000
else
  port=80
fi
vagrant destroy -f $env
vagrant up $env
server_name=$(vagrant ssh-config $env | grep HostName | awk \{'print $2'\})
sleep 5
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  --disable-application-cache "http://${server_name}:${port}"
