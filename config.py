import os
import sys

from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir + '/mod_auth/')
sys.path.insert(0, project_dir + '/data/')


class BaseConfig(object):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://{}:{}@{}/devopsloft" \
        .format(os.getenv('MYSQL_USER', 'application'), os.getenv('MYSQL_PASSWORD', 'application'), os.getenv('MYSQL_HOST', 'mysql'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
