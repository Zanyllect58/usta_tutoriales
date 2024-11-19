from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()
mysql = MySQL()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('admin', 'student', 'teacher'), nullable=False)
    identificacion = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)  # Add this line
    career = db.Column(db.String(120))
    semester = db.Column(db.String(120))