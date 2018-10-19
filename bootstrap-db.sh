#!/bin/bash

export DEBIAN_FRONTEND=noninteractive

echo "Getting updates..."
apt-get update

echo "Setup mysql root password..."
debconf-set-selections <<< 'mysql-server mysql-server/root_password password 12345'
debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password 12345'

echo "Mysql installation..."
apt-get install -y mysql-server libmysqlclient-dev expect

echo "Mysql service start..."
systemctl restart mysql

unbuffer expect -c "
spawn mysql_config_editor set --login-path=local --host=localhost --user=root --password
expect -nocase \"Enter password:\" {send \"12345\r\"; interact}"

echo "Create application database and users table"
mysql --login-path=local -e "CREATE DATABASE devopsloft;"
mysql --login-path=local -e "CREATE TABLE devopsloft.users (first_name varchar(100) NOT NULL,last_name varchar(100) NOT NULL,email VARCHAR(320) NOT NULL);"

echo "db boostrap script completed!"
