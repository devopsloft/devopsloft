import os
import sqlalchemy as db

connection_string = "mysql+mysqlconnector://{}:{}@{}/devopsloft" \
    .format(
            os.getenv('MYSQL_USER', 'application'),
            os.getenv('MYSQL_PASSWORD', 'application'),
            os.getenv('MYSQL_HOST', 'mysql')
    )


class Member:
    def __init__(self, email=None, member_type=None,
                 password_last_change_date=None, member_status=None):
        self.email = email
        self.member_type = member_type
        self.password_last_change_date = password_last_change_date
        self.member_status = member_status


def get_member_status(email):
    engine = db.create_engine(connection_string)

    connection = engine.connect()
    metadata = db.MetaData()

    users_table = \
        db.Table('users', metadata, autoload=True, autoload_with=engine)

    filtered_query = \
        db.select([users_table]).where(users_table.columns.email == email)

    filtered_result_proxy = connection.execute(filtered_query)

    result_set = filtered_result_proxy.fetchall()

    return result_set
