import sqlite3

con = sqlite3.connect('../data.db')
cur = con.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, user_name text, password text)"
cur.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cur.execute(create_table)

select_query = "SELECT * FROM items"
cur.execute(select_query)

con.commit()
con.close()
