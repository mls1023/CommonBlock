import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'my-secret-key'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/CommonBlock_Users'
    SQLALCHEMY_TRACK_MODIFICATIONS = False