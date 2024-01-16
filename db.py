import sqlite3
import utils.config as configurations

from utils.log_message import log_message
from utils.clear_config import clear_configurations
from utils.prepare_recipe_object import prepare_recipe_object
from utils.randomizer import random_heart


async def save_recipe(chat_id, bot):
    try:
        recipe_object = prepare_recipe_object()
        # cur = configurations.db_con.cursor()
        sqlite_insert_query = (f"INSERT INTO recipes (name, recipe_type, description, photo_path) VALUES "
                               f"('{recipe_object.name.lower()}','{recipe_object.recipe_type}',"
                               f"'{recipe_object.description}','{recipe_object.photo_path}')")
        log_message(sqlite_insert_query)
        # cur.execute(sqlite_insert_query)
        # configurations.db_con.commit()
        log_message("Record inserted successfully into table")
        await bot.send_message(chat_id,
                               "Рецепт успешно сохранён! Приятного приготовления и аппетита! " + random_heart())

    except sqlite3.Error as error:
        await bot.send_message(chat_id, "Произошла ошибка! Обратитесь к Игорю для исправления! 🤷")
        print("Failed to insert data into sqlite table", error)
    finally:
        if configurations.db_con:
            configurations.db_con.close()
            clear_configurations()
            print("The SQLite connection is closed")


def get_categories():
    cur = configurations.db_con.cursor()
    return cur.execute('SELECT * FROM types WHERE has_parent=0')


def get_category_item(recipe):
    cur = configurations.db_con.cursor()
    return cur.execute('SELECT * FROM recipes WHERE recipe_type="' + recipe + '"')


async def delete_item(chat_id, bot):
    try:

        cur, name, description = configurations.db_con.cursor(), configurations.transaction_data[0], \
            configurations.transaction_data[2]
        delete_query = 'DELETE FROM recipes WHERE name="' + name.lower() + '" AND description="' + description.lower() + '"'
        cur.execute(delete_query)
        configurations.db_con.commit()
        cur.close()
    except sqlite3.Error as error:
        await bot.send_message(chat_id, "Произошла ошибка! Обратитесь к Игорю для исправления! 🤷")
        print("Failed to delete data into sqlite table", error)
    finally:
        if configurations.db_con:
            configurations.db_con.close()
            clear_configurations()
            print("The SQLite connection is closed")


async def update_item(chat_id, bot):
    configurations.set_action = False
    configurations.start = True
    recipe_object = configurations.recipe_object
    if recipe_object.photo_path is not None:
        photo_string = str(recipe_object.photo_path).replace('[', '').replace(']', '').replace("'", "")
    else:
        photo_string = "NULL"
    try:

        cur, prev_name, prev_description = configurations.db_con.cursor(), configurations.transaction_data[0], \
            configurations.transaction_data[
                2]
        name, description = configurations.recipe_object.name, configurations.recipe_object.description,
        uq = (
                'UPDATE recipes SET name="' + name.lower() + '", description="' + description.lower() + '", photo_path="' +
                photo_string + '" WHERE name="' + prev_name.lower() + '" AND description="' + prev_description.lower() + '"')
        cur.execute(uq)
        configurations.db_con.commit()
        await bot.send_message(chat_id, "Рецепт успешно обновлён! Важно держать рецепты актуальными! 💛")
    except sqlite3.Error as error:
        await bot.send_message(chat_id, "Произошла ошибка! Обратитесь к Игорю для исправления! 🤷")
        print("Failed to delete data into sqlite table", error)
    finally:
        if configurations.db_con:
            configurations.db_con.close()
            clear_configurations()
            print("The SQLite connection is closed")
