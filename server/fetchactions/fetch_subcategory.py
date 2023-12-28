from sqlite3 import Cursor, Connection

from server.communication import connect, disconnect
from utils.log_message import log_message


def fetch_subcategory(recipe_type: str):
    subcategories: list | None = None
    connection: Connection | None = None
    log_message(message='fetching subcategories...')
    try:
        connection = connect()
        cursor: Cursor = connection.cursor()
        subcategories = cursor.execute(f'SELECT * FROM types WHERE parent_name="{recipe_type}"').fetchall()
    except Exception:
        raise IOError('Error getting subcategories')
    finally:
        log_message(message='fetch_subcategories call is disconnected')
        disconnect(connection)
        return subcategories
