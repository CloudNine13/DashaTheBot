import pathlib
import sqlite3
from sqlite3 import Connection

import utils.config as configurations


def connect():
    if configurations.db_con is None:
        database = pathlib.Path('recipes.db')
        configurations.db_con = sqlite3.connect(database)
    return configurations.db_con


def disconnect(connection: Connection | None):
    if connection is None:
        return
    connection.close()
    configurations.db_con = None
