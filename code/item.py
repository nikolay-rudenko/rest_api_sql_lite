import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class Item(Resource):
    purser = reqparse.RequestParser()
    purser.add_argument('price', type=float, required=True, help='This field cannot left blank!')

    @jwt_required()
    def get(self, name):
        item = self.find_by_name(name)

        if item:
            return item
        return {'message': 'Item not exist'}, 404

    @classmethod
    def find_by_name(cls, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cur.execute(query, (name,))
        row = result.fetchone()
        con.close()

        if row:
            return {"item": {'name': row[0], 'price': row[1]}}


    def post(self, name):
        if self.find_by_name(name):
            return {"message": f"item '{name}' already exist"}, 400

        data = Item.purser.parse_args()

        item = {'name': name, 'price': data['price']}

        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "INSERT INTO items VALUES (?, ?)"
        cur.execute(query_insert, (item['name'], item['price']))

        con.commit()
        con.close()

        return item, 201

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