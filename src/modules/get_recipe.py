import os
import sqlite3
from sqlite3 import Error
from pathlib import Path

from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv())
database_path = os.environ["DATABASE_PATH"]


def get_recipe(chat_id, context):
    conn = None
    try:
        base_dir = Path(__file__).resolve().parent.parent.parent
        database_dir = os.path.join(base_dir, database_path)
        conn = sqlite3.connect(database_dir)


    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        pass
