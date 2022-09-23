import sqlite3

con = sqlite3.connect('users.db')
cur = con.cursor()


def remove_users(users):
    for user in users:
        cur.execute("UPDATE poll SET is_play = ? WHERE username = ?", (0, user))

    con.commit()
