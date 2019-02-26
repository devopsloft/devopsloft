#!/usr/bin/env bash

mysql -uroot -p${MYSQL_ROOT_PASSWORD} <<-EOSQL
CREATE USER IF NOT EXISTS 'exporter'@'%' IDENTIFIED BY '${MYSQL_EXPORTER_PASSWORD:-exporter}';
ALTER USER 'exporter'@'%' IDENTIFIED BY '${MYSQL_EXPORTER_PASSWORD:-exporter}';
EOSQL