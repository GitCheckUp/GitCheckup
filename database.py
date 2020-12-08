from config import *
import sqlite3
db_conn = sqlite3.connect(db_path)

class db_op(object):
    def initialize_table_recent_repos():
        with db_conn:
            db_cur = db_conn.cursor()
            db_cur.execute("""CREATE TABLE IF NOT EXISTS recent_repos(
            id PRIMARY KEY  NOT NULL,
            url TEXT UNIQUE);""")