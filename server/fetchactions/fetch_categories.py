from sqlite3 import Cursor, Connection

from server.communication import connect, disconnect
from utils.log_message import log_message


def fetch_categories() -> list:
    categories: list | None = None
    connection: Connection | None = None
    log_message(message='fetching categories...')
    try:
        connection = connect()
        cursor: Cursor = connection.cursor()
        categories = cursor.execute('SELECT * FROM types WHERE has_parent=0').fetchall()
    except Exception:
        raise IOError('Error getting categories')
    finally:
        log_message(message='fetch_categories call is disconnected')
        disconnect(connection)
        return categories
