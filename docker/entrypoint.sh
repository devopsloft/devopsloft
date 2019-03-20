#!/usr/bin/env bash

set -e

service mysql start
python3 application.py $1 $2 $3
