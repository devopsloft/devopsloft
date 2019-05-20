#!/usr/bin/env bash

set -ex

BASE_FOLDER=$1

mkdir /tmp/.devopsloft
apt-get update
apt-get install -y mysql-client python3-pip

pip3 install -r $BASE_FOLDER/requirements.txt
