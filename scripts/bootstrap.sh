#!/usr/bin/env bash

set -e

BASE_FOLDER=$1

mkdir -p /tmp/.devopsloft
apt-get update
apt-get install -y mysql-client python3-pip

pip3 install -r $BASE_FOLDER/requirements.txt
