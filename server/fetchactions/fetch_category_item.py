from sqlite3 import Cursor, Connection
from server.communication import connect, disconnect
from utils.log_message import log_message


def fetch_category_items(recipe_type: str) -> list:
    category_items: list | None = None
    connection: Connection | None = None
    log_message(message='fetching category items...')
    try:
        connection = connect()
        cursor: Cursor = connection.cursor()
        category_items = cursor.execute(f'SELECT * FROM recipes_fts WHERE recipe_type="{recipe_type}"').fetchall()
    except Exception:
        raise IOError('Error getting category items')
    finally:
        disconnect(connection)
        return category_items
