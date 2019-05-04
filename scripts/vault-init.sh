#!/usr/bin/env bash

set -ex

sleep 10
# shellcheck source=/dev/null
source $1/.env
export VAULT_ADDR=http://127.0.0.1:$VAULT_GUEST_PORT
docker exec -i vault sh -c "vault operator init -key-shares=5 -key-threshold=3 --address=$VAULT_ADDR" > keys.txt
while read line; do
  unseal_key=$(echo $line | awk '{print $4}')
  docker exec vault sh -c "export VAULT_ADDR=$VAULT_ADDR; vault operator unseal $unseal_key"
done <<<"$(head -n5 keys.txt)"
VALUT_TOKEN=$(cat keys.txt | awk 'NR == 7 {print $4}')
export VALUT_TOKEN
docker exec -i vault sh -c "export VALUT_TOKEN=$VALUT_TOKEN; export VAULT_ADDR=$VAULT_ADDR; echo $VALUT_TOKEN > ~/.vault-token; vault secrets enable -path=secret kv; vault write secret/content value=secretData"
