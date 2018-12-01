#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

echo "Getting updates..."
apt-get update

# echo "Installing Python3..."
# apt-get install -y python3

echo "Installing pip..."
apt-get install -y python3-pip

echo "Upgrading pip..."
pip3 install --upgrade pip

# echo "Installing mysql-connector-python..."
# pip3 install mysql-connector-python

echo "Installing virtualenv..."
pip install virtualenv

echo "Setting virtual environment..."
virtualenv -p python3 venv
source venv/bin/activate

uname -r | grep aws
if [ $? -eq 0 ]; then
	echo 'aws'
	cd devopsloft
else
	echo 'not aws'
	cd /vagrant
fi

echo "Installing additional pips from requirements.txt..."
pip install -r requirements.txt

nohup python3 application.py > /dev/null 2>&1 &

echo "application boostrap script completed!"
