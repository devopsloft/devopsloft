import mysql.connector

config = {
    'user': 'root',
    'password': '12345',
    'host': 'localhost',
    'database': 'devopsloft',
    'raise_on_warnings': True
} 

def is_email_exists (  email):
    cnx = mysql.connector.connect(**config)
    
    cursor = cnx.cursor()

    query = "SELECT count(*) AS count_users FROM users WHERE email ='" + email + "'"

    cursor.execute(query)
    
    myresult = cursor.fetchall()

    cursor.close()

    isExistsEmail = False

    # loop should run once

    for (count_users) in myresult:
        isExistsEmail = count_users[0] != 0

    print(isExistsEmail)

    cursor.close()
    cnx.close()

    # better way but didn't work

    # query = ("SELECT first_name, last_name FROM users "
    #      "WHERE first_name ='%s'")
    # cursor.execute(query, (first_name))

is_email_exists('email@aaa.com')

