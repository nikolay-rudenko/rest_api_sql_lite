import sqlite3

# initialize the connection
connection = sqlite3.connect('data.db')

# responsible of selecting, running, storing the result
cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, user_name text, password text)"

cursor.execute(create_table)
insert_query = "INSERT INTO users VALUES(?, ?, ?)"

users = [
    (1, 'cat', 'qwer'),
    (2, 'tom', 'asdf'),
    (3, 'jack', 'zxcv')
]

cursor.executemany(insert_query, users)
connection.commit()

select_query = "SELECT * FROM users"
cursor.execute(select_query)
print(cursor.fetchall())

connection.close()
