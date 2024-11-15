import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'usta_2024'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@localhost/users_db'    
    SQLALCHEMY_TRACK_MODIFICATIONS = False