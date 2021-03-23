import pdb
import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from source_code.models.item_model import ItemModel


class Item(Resource):
    purser = reqparse.RequestParser()
    purser.add_argument('price', type=float, required=True, help='This field cannot left blank!')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item
        return {'message': 'Item not exist'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {"message": f"item '{name}' already exist"}, 400

        data = Item.purser.parse_args()

        item = ItemModel(name, data['price'])

        try:
            ItemModel.save_to_db(item)
        except:
            return {"message": f"An error occurs inserting item.{item}"}, 500  # internal server error

        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()

        return {'message': f'Item {name} deleted'}

    def put(self, name):
        data = Item.purser.parse_args()
        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'])
        else:
            item.price = data['price']
        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "SELECT * FROM items"
        result = cur.execute(query_insert)
        items = []
        for row in result:
            items.append({'name': row[0], 'price': row[1]})
        con.commit()
        con.close()

        return {"items": items}
