import os


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///userinfo.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

