from config import *
import sqlite3
try:
    db_conn = sqlite3.connect(db_path)
except:
    print("ERROR: Could not initialize or access the database. Check permissions.")
class Db_op(object):
    def initialize_table_recent_repos():
        with db_conn:
            db_cur = db_conn.cursor()
            db_cur.execute("""CREATE TABLE IF NOT EXISTS recent_repos(
            id PRIMARY KEY  NOT NULL,
            url TEXT UNIQUE);""")
    
    def add_to_recent_repos(url):
        db_cur=db_conn.cursor()
        with db_conn:
            db_cur.execute("INSERT INTO recent_repos VALUES (NULL,?)",(url,))
            db_conn.commit()
        