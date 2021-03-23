from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from source_code.security import authenticate, identity
from source_code.resources.user import UserRegister
from source_code.resources.item import Item, ItemList
from source_code.db import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
api = Api(app)
app.secret_key = 'nikolay'

db.init_app(app)


# initialization JWT object
jwt = JWT(app, authenticate, identity)
# JWT creating new endpoint /auth, when we call /auth we send pass and login

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
