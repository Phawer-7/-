import sqlite3

con = sqlite3.connect("users.db")
cur = con.cursor()


class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, username, id):
        data  = []
        with self.connection:
            with self.connection:
                return self.cursor.executemany("INSERT INTO pool VALUES(?, ?)", [(username, id),] )

    def get_users(self):
        with self.connection:
            res = self.cursor.execute("SELECT username FROM pool")
            return res.fetchall()

    def close(self):
        self.connection.close()
