#!/usr/bin/env bash

set -ex

cp $2/.env $2/app_s2i/
cp $2/.env $2/db_s2i/
