#!/bin/bash
source /vagrant/venv/bin/activate
cd /vagrant
python3 application.py $1 $2 $3 </dev/null >/dev/null 2>&1 &
