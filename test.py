import sqlite3 as sql

conn = sql.connect('users.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE users(
              id TEXT PRIMARY KEY,
              phone TEXT,
              is_auth INTEGER,
              is_joined INTEGER
          )""")

conn.commit()
conn.close()
