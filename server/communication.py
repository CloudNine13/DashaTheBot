import pathlib
import sqlite3
import utils.config as configurations

from sqlite3 import Connection
from utils.log_message import log_message


def connect():
    if configurations.db_con is None:
        database = pathlib.Path('recipes.db')
        configurations.db_con = sqlite3.connect(database)
        log_message('SQL Database has been connected!')
    return configurations.db_con


def disconnect(connection: Connection | None):
    if connection is None:
        return
    connection.close()
    configurations.db_con = None
    log_message('SQL Database connection is closed!')
