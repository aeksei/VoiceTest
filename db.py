import sqlite3

DATABASE = "VoiceDB.db"


class VoiceDB:
    def __init__(self, database):
        self.conn = sqlite3.connect(database, check_same_thread = False)
        self.cur = self.conn.cursor()

        sql = '''CREATE TABLE if not exists users (
        "uid" INTEGER PRIMARY KEY, 
        "username" TEXT)'''
        self.query(sql)

    def __del__(self):
        self.conn.close()

    def query(self, sql, args=[]):
        self.cur.execute(sql, args)
        self.conn.commit()
        return self.cur

    def get_users(self):
        return [u[0] for u in self.query("SELECT uid FROM users")]

    def create_voice_table(self, uid):
        sql = '''CREATE TABLE if not exists voices_by_{} (
        "id"   INTEGER PRIMARY KEY AUTOINCREMENT,
        "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
        "voice"  BLOB NOT NULL
        );'''.format(uid)
        self.query(sql)

    def add_user(self, uid, username):
        self.query('INSERT INTO users VALUES(?, ?);', [uid, username])
        self.create_voice_table(uid)

    def write_voice(self, uid, voice):
        sql = "INSERT INTO voices_by_{uid} (voice) VALUES(?);".format(uid=uid)
        self.query(sql, [sqlite3.Binary(voice)])


if __name__ == "__main__":
    db = VoiceDB(DATABASE)
    users = db.get_users()
    uid = 1234
    if uid in users:
        db.add_user(uid, "test")
    with open("main.py", "rb") as input_file:
        ablob = input_file.read()
        db.write_voice(1234, ablob)
