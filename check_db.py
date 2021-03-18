import sqlite3

con = sqlite3.connect('data.db')
cur = con.cursor()

query = "PRAGMA table_info(items)"
cur.execute(query)
print(cur.fetchall())

con.commit()
con.close()