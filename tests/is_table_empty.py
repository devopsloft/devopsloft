#!/usr/bin/env python3

import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv()

config = {
    'user': os.getenv('MYSQL_USER'),
    'password': os.getenv('MYSQL_PASSWORD'),
    'host': '127.0.0.1',
    'database': os.getenv('MYSQL_DATABASE'),
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
