import sqlite3
from datetime import datetime

DATABASE = "VoiceDB.db"


class VoiceDB:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)  # или :memory: чтобы сохранить в RAM
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE if not exists users (
            "uid" INTEGER PRIMARY KEY, 
            "username" TEXT)''')
        self.conn.commit()

    def create_voice_table(self, uid):
        self.cursor.execute(
            '''CREATE TABLE if not exists voices_by_{} (
            "id"   INTEGER PRIMARY KEY AUTOINCREMENT,
            "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
            "voice"  BLOB NOT NULL
            );'''.format(uid))
        self.conn.commit()

    def add_user(self, uid, username):
        self.cursor.execute('INSERT INTO users VALUES(?, ?);', (uid, username))
        self.create_voice_table(uid)
        self.conn.commit()

    def write_voice(self, uid, voice):
        sql = "INSERT INTO voices_by_{uid} (voice) VALUES(?);".format(uid=uid)
        self.cursor.execute(sql, [sqlite3.Binary(voice)])
        self.conn.commit()


if __name__ == "__main__":
    db = VoiceDB(DATABASE)
    db.add_user(123, "test")
    with open("main.py", "rb") as input_file:
        ablob = input_file.read()
        db.write_voice("123", ablob)
