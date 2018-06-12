import os, sys

from os import path
sys.path.append(path.dirname( path.dirname( path.abspath(__file__))))

project_dir = os.path.dirname(os.path.abspath(__file__))
# project_dir2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir + '/mod_auth/')
sys.path.insert(0, project_dir + '/data/')

class BaseConfig(object):
    SECRET_KEY = "devops"
    # SQLALCHEMY_DATABASE_URI = "sqlite:////home/kubkub/github/DevOpsLoft/data/usersdatabase.db"
    SQLALCHEMY_DATABASE_URI = "sqlite:///{}".format(os.path.join(project_dir, "data/usersdatabase.db"))
    SQLALCHEMY_TRACK_MODIFICATIONS = False