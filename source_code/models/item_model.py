import sqlite3
from source_code.db import db


class ItemModel(db.Model):
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def json(self):
        return {'name': self.name, 'price': self.price}

    @classmethod
    def find_by_name(cls, name):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query = 'SELECT * FROM items WHERE name=?'
        result = cur.execute(query, (name,))
        row = result.fetchone()
        con.close()

        if row:
            return {'price': row[0], 'name': row[1]}

    def insert(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "INSERT INTO items VALUES (?, ?)"
        cur.execute(query_insert, (self.name, self.price))

        con.commit()
        con.close()

    def update(self):
        con = sqlite3.connect('data.db')
        cur = con.cursor()

        query_insert = "UPDATE items SET price=? WHERE name=?"
        cur.execute(query_insert, (self.price, self.name))

        con.commit()
        con.close()
