from sqlite3 import Cursor, Connection
from server.communication import connect, disconnect
from utils.log_message import log_message


def fetch_all_recipes() -> Cursor | None:
    all_recipes: list | None = None
    connection: Connection | None = None
    log_message(message='fetching all recipes...')
    try:
        connection = connect()
        cursor: Cursor = connection.cursor()
        all_recipes = cursor.execute('''SELECT * FROM recipes_fts''').fetchall()
    except Exception:
        raise IOError('Error getting all recipes')
    finally:
        log_message(message='fetch_all_recipes call is disconnected')
        disconnect(connection)
        return all_recipes
