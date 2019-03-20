#!/usr/bin/env python3

import mysql.connector
import os

config = {
    'user': os.environ['mysql_root_username'],
    'password': os.environ['mysql_root_password'],
    'host': 'localhost',
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
