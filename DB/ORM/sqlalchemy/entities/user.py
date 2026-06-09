import sqlalchemy

from database import db

class User(db.base):
    __tablename__ = 'users'

    userid = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    useremail = sqlalchemy.Column(sqlalchemy.String, unique=True, nullable=False)
    password = sqlalchemy.Column(sqlalchemy.String, nullable=False)