from sqlite3 import Cursor, Connection
from server.communication import connect, disconnect
from utils.log_message import log_message


def fetch_recipe_by_name(name: str):
    recipes_by_name: list | None = None
    connection: Connection | None = None
    log_message(message='fetching recipes by name...')
    try:
        connection = connect()
        cursor: Cursor = connection.cursor()
        recipes_by_name = cursor.execute(f'SELECT * FROM recipes_fts WHERE name MATCH "{name}*"').fetchall()
    except Exception:
        raise IOError('Error getting categories')
    finally:
        disconnect(connection)
        return recipes_by_name
