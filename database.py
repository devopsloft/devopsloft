import mysql.connector

config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': 'devopsloft',
    'raise_on_warnings': True
}


def is_email_exists(email):
    cnx = mysql.connector.connect(**config)

    cursor = cnx.cursor()
    query = "SELECT count(*) AS count_users FROM users WHERE email ='" + email + "'"
    cursor.execute(query)

    query_result = cursor.fetchall()
    cursor.close()
    cnx.close()

    is_exists_email = False

    # loop should run once.
    for (count_users) in query_result:
        is_exists_email = count_users[0] != 0

    return is_exists_email

    # better way but didn't work

    # query = ("SELECT first_name, last_name FROM users "
    #      "WHERE first_name ='%s'")
    # cursor.execute(query, (first_name))


# test functionality
print(is_email_exists('myemail@gmail.com'))
