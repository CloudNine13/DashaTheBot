import utils.config as configurations

from sqlite3 import Cursor, Connection
from server.communication import connect, disconnect
from utils.log_message import log_message


def delete_recipe() -> str:
    name = configurations.data_to_modify[0]
    recipe_type = configurations.data_to_modify[1]
    description = configurations.data_to_modify[2]

    connection: Connection | None = None
    log_message(message=f'Deleting a recipe {name}...')
    try:
        connection = connect()
        cursor: Cursor = connection.cursor()
        cursor.execute('''DELETE FROM recipes_fts WHERE name=? AND recipe_type=? AND description=?''',
                       (name, recipe_type, description))
        connection.commit()
    except Exception:
        raise IOError(f'Error deleting a recipe {name} from {recipe_type}')
    finally:
        disconnect(connection)
        return name
