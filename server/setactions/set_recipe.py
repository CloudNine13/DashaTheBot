import sqlite3
from sqlite3 import Error

from server.communication import connect, disconnect
from utils.clear_config import clear_configurations
from utils.log_message import log_message
from utils.prepare_recipe_object import prepare_recipe_object
from utils.randomizer import random_heart


async def set_recipe(chat_id, bot):
    connection = connect()
    try:
        cursor = connection.cursor()
        recipe_object = prepare_recipe_object()
        cursor.execute(f"INSERT INTO recipes_fts (name, recipe_type, description, photo_path) VALUES "
                       f"('{recipe_object.name}','{recipe_object.recipe_type}',"
                       f"'{recipe_object.description}', ?)",
                       (recipe_object.photo_path,))
        connection.commit()
        log_message("Record inserted successfully into table")
        await bot.send_message(chat_id, "Рецепт успешно сохранён! "
                                        f"Приятного приготовления и аппетита! {random_heart()}")

    except Error as error:
        log_message("Failed to insert data into sqlite table",
                    f"{error.sqlite_errorname} {error.sqlite_errorcode}")
        await bot.send_message(chat_id, "Произошла ошибка! Обратитесь к Игорю для исправления! 🤷")
    finally:
        disconnect(connection)
        clear_configurations()
        print("The SQLite connection is closed")
