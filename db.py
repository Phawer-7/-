import sqlite3


class SQLighter:
    def __init__(self, database_file):
        self.connection = sqlite3.connect(database_file)
        self.cursor = self.connection.cursor()

    def add_user(self, username, user_id, is_play):
        with self.connection:
            return self.cursor.executemany("INSERT INTO poll VALUES(?, ?, ?)",
                                           [(user_id, is_play, username,),] )

    def check_act(self, username):
        with self.connection:
            result = self.cursor.execute('SELECT is_play FROM poll WHERE username = ?', (username,))
            return result.fetchone()[0]

    def get_users(self):
        with self.connection:
            res = self.cursor.execute("SELECT username FROM poll")
            who_play = []
            for k in res.fetchall():
                if self.check_act(k[0]):
                    who_play.append(k[0])

            return who_play

    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM poll WHERE user_id = ?", (user_id,)).fetchall()
            return bool(len(result))

    def remove_users(self):
        with self.connection:
            for user in self.get_users():
                return self.cursor.execute("UPDATE poll SET is_play = ? WHERE username = ?", (0, user))

    def update_username(self, username, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE poll SET username = ? WHERE user_id = ?", (username, user_id))

    def user_play(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE poll SET is_play = ? WHERE user_id = ?", (1, user_id))

    def remove_user(self, user_id):
        with self.connection:
            return self.cursor.execute("UPDATE poll SET is_play = ? WHERE user_id = ?", (0, user_id))

    def close(self):
        self.connection.close()
