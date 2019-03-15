#!/usr/bin/env python
import mysql.connector
import yaml


def load_config(config_file):
    with open(config_file, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


cfg = load_config('provisioning/playbooks/group_vars/all.yml')

config = {
    'user': cfg['mysql_root_username'],
    'password': cfg['mysql_root_password'],
    'host': cfg['mysql_bind_address'],
    'database': 'devopsloft',
    'raise_on_warnings': True
}


def is_table_empty(table):
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()
    query = ("SELECT COUNT(*) FROM %s" % table)
    cursor.execute(query, ())

    row_count = cursor.fetchone()[0]
    print("number of rows in {}: {}".format(table, row_count))
    exit(row_count)

    cursor.close()
    cnx.close()


if __name__ == "__main__":
    is_table_empty("users")
