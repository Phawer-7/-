import sqlite3

con = sqlite3.connect("users.db")
cur = con.cursor()


class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, username, id):
        data = []
        with self.connection:
            with self.connection:
                return self.cursor.executemany("INSERT INTO pool VALUES(?, ?)", [(username, id),] )

    def get_users(self):
        with self.connection:
            res = self.cursor.execute("SELECT username FROM pool")
            return res.fetchall()

    def user_exists(self, username):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM pool WHERE username = ?", (username,)).fetchall()
            return bool(len(result))

    def remove_users(self):
        pass

    def remove_user(self):
        pass

    def close(self):
        self.connection.close()
