import sqlite3

con = sqlite3.connect('../data.db')
cur = con.cursor()

create_table = "CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, user_name text, password text)"
cur.execute(create_table)

insert_query = "INSERT INTO users VALUES(?, ?, ?)"
user = (1, 'cat', 'qwer')
cur.execute(insert_query, user)

select_query = "SELECT * FROM users"
cur.execute(select_query)
print(cur.fetchall())

con.commit()
con.close()
