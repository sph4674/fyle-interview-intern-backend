import os

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret@secret12345'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'mysql://Fyle:Fyle@localhost:3306/fyle'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
