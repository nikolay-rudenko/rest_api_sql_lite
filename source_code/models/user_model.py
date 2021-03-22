import sqlite3
from source_code.db import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80))
    password = db.Column(db.String(80))

    def __init__(self, _id, user_name, password):
        self.id = _id
        self.user_name = user_name
        self.password = password

    @classmethod
    def find_by_user_name(cls, user_name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE user_name=?'
        result = cursor.execute(query, (user_name,))

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_user_id(cls, _id):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = 'SELECT * FROM users WHERE id=?'
        result = cursor.execute(query, (_id,))

        row = result.fetchone()
        if row:
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user