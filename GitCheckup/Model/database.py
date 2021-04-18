import sqlite3
from Model.config import Config
print(Config.db_path)
class Database:
    def __init__(self):
        self.db_conn = sqlite3.connect(Config.db_path)

    def initialize_table_recent_repos(self):
        with self.db_conn:
            db_cur = self.db_conn.cursor()
            db_cur.execute("""CREATE TABLE IF NOT EXISTS recent_repos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url char(80) UNIQUE);""")

    def add_to_recent_repos(self,url):
        db_cur=self.db_conn.cursor()
        with self.db_conn:
            try:
                db_cur.execute("INSERT INTO recent_repos(url) VALUES (?)",(url,))
                self.db_conn.commit()
            except sqlite3.IntegrityError:
                pass #URL already exists.