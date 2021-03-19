import sqlite3
import pdb

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

        try:
            self.insert(item)
        except:
            return {"message": f"An error occurs inserting item.{item}"}, 500  # internal server error

        return item, 201

    @classmethod
    def insert(cls, item):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "INSERT INTO items VALUES (?, ?)"
        cur.execute(query_insert, (item['name'], item['price']))

        con.commit()
        con.close()

    @jwt_required()
    def delete(self, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "DELETE FROM items WHERE name=?"
        cur.execute(query_insert, (name,))

        con.commit()
        con.close()

        return {'message': f'Item {name} deleted'}

    def put(self, name):
        data = Item.purser.parse_args()
        item = self.find_by_name(name)
        updated_item = {'name': name, 'price': data['price']}

        if item is None:
            try:
                self.insert(updated_item)
            except:
                return {"message": f"An error occurs inserting item.{updated_item}"}, 500
        else:
            try:
                self.update(updated_item)
            except:
                return {"message": f"An error occurs inserting item.{updated_item}"}, 500

        return updated_item

    @classmethod
    def update(cls, item):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "UPDATE items SET price=? WHERE name=?"
        cur.execute(query_insert, (item['price'], item['name']))

        con.commit()
        con.close()


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
