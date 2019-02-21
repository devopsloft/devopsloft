#!/usr/bin/env bash
source /vagrant/venv/bin/activate
cd /vagrant
python3 application.py </dev/null >/dev/null 2>&1 &