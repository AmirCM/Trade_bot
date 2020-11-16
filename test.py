import sqlite3 as sql
from user import User

conn = sql.connect('users.db')
cur = conn.cursor()
sar = User('amir_ahb', '09387151079')
sar.is_joined = True
with conn:
    cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", sar.get_data())
print(sar.get_data(), type(sar.get_data()))
cur.execute("SELECT * FROM users")
print(cur.fetchall())
