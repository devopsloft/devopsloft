#!/usr/bin/env bash

mysql -uroot -p${MYSQL_ROOT_PASSWORD} <<-EOSQL
CREATE USER IF NOT EXISTS '${MYSQL_USER:-application}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD:-application}';
ALTER USER '${MYSQL_USER:-application}'@'%' IDENTIFIED BY '${MYSQL_PASSWORD:-application}';
GRANT ALL on devopsloft.* TO '${MYSQL_USER:-application}'@'%'
EOSQL