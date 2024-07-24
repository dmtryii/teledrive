import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')

    BOT_TOKEN = os.environ.get('BOT_TOKEN')

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    JWT_TOKEN_LOCATION = ['headers']
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    