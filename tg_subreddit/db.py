from loguru import logger
import sqlite3

from .config import database_table_name_reddit_post


logger = logger.bind(service='db')


def prepare_db(database_path: str):
    logger.info(f'preparing database {database_path}')

    conn = sqlite3.connect(database_path) 
    cur = conn.cursor()

    logger.debug(f'preparing table {database_table_name_reddit_post}')
    cur.execute(f'''
    CREATE TABLE IF NOT EXISTS {database_table_name_reddit_post} (
        id varchar(128) PRIMARY KEY,
        content text
    )
''')
    logger.info(f'prepared table {database_table_name_reddit_post}')

    conn.commit()
    conn.close()

    logger.info('database prepared')