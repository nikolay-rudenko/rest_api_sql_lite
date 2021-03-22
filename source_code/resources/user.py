import sqlite3
from flask_restful import Resource, reqparse
from source_code.models.user_model import UserModel


class UserRegister(Resource):
    purser = reqparse.RequestParser()
    purser.add_argument('user_name', type=str, required=True, help='This field cannot left blank!')
    purser.add_argument('password', type=str, required=True, help='This field cannot left blank!')

    def post(self):
        data = self.purser.parse_args()

        if UserModel.find_by_user_name(data['user_name']):
            return {"message": "A user with that user name already exist"}, 400

        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cur.execute(query, (data['user_name'], data['password']))

        con.commit()
        con.close()

        return {"message": f"User {data['user_name']} created successfully!"}, 201






