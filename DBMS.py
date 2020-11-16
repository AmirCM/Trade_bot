import sqlite3 as sql
from user import User


class DBMS:
    def __init__(self):
        self.conn = sql.connect('users.db')
        self.cur = self.conn.cursor()

    def update_user(self, rec: User):
        with self.conn:
            self.cur.execute("""UPDATE users 
                        SET phone = :phone,
                            is_auth =:is_auth,
                            is_joined =:is_joined
                        WHERE id = :id """,
                             {'id': rec.username, 'phone': rec.phone, 'is_auth': rec.is_auth,
                              'is_joined': rec.is_joined})

    def insert_user(self, rec: User):
        with self.conn:
            self.cur.execute("INSERT INTO users VALUES (?, ?, ?, ?)", rec.get_data())

    def remove_user(self, rec: User):
        with self.conn:
            self.cur.execute("DELETE from main.users WHERE id = (?)", (rec.username,))

    def delete_table(self):
        with self.conn:
            self.cur.execute("DELETE FROM main.users")

    def show_users(self):
        self.cur.execute("SELECT * FROM users")
        print(self.cur.fetchall())

    def get_user(self, username: str):
        with self.conn:
            self.cur.execute("select * from main.users WHERE id = (?)", (username,))
        return self.cur.fetchone()

    def get_users(self):
        with self.conn:
            self.cur.execute("SELECT * FROM users")
        return self.cur.fetchall()
