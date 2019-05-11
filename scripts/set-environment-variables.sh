#!/usr/bin/env bash

set -ex

sed -i -n -e '/^ENVIRONMENT=/!p' -e '$aENVIRONMENT='$1 $2/.env
cp $2/.env $2/app_s2i/
cp $2/.env $2/db_s2i/
