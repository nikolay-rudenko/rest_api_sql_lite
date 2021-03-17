import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    purser = reqparse.RequestParser()
    purser.add_argument('price', type=float, required=True, help='This field cannot left blank!')


    @jwt_required()
    def get(self, name):
        # next giving the first item that found
        item = next(filter(lambda i: i['name'] == name, items), None)

        return {"item": item}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda i: i['name'] == name, items), None):
            return {"message": f"item '{name}' already exist"}, 400

        data = Item.purser.parse_args()

        item = {'name': name, 'price': data['price']}
        items.append(item)

        return items, 201

    @jwt_required()
    def delete(self, name):
        global items
        items = list(filter(lambda x: x['name'] != name, items))

        return {'message': f'Item {name} deleted'}

    def put(self, name):
        data = Item.purser.parse_args()

        item = next(filter(lambda x: x['name'] == name, items), None)

        if item == None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item


class ItemList(Resource):
    def get(self):
        if len(items) > 0:
            return {'items': items}
        else:
            return {"items": None}, 404