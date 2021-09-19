import sqlite3


def prepare_db(database_path: str):
    conn = sqlite3.connect(database_path) 
    cur = conn.cursor()

    cur.execute('''
    CREATE TABLE IF NOT EXISTS reddit_post (
        id varchar(128) PRIMARY KEY,
        content text
    )
''')

    conn.commit()
    conn.close()