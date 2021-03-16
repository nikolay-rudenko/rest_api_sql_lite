import sqlite3
from flask_restful import Resource, reqparse
import pdb


class User:
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


class UserRegister(Resource):
    purser = reqparse.RequestParser()
    purser.add_argument('user_name', type=str, required=True, help='This field cannot left blank!')
    purser.add_argument('password', type=str, required=True, help='This field cannot left blank!')

    def post(self):
        data = self.purser.parse_args()

        con = sqlite3.connect('data.db')
        cur = con.cursor()
        pdb.set_trace()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"

        cur.execute(query, (data['user_name'], data['password']))

        con.commit()
        con.close()

        return {"message": "User created successfully!"}, 201



