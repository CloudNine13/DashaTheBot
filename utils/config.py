import os
import cloudinary
import nest_asyncio

from sqlite3 import Connection
from dotenv import load_dotenv
from models.recipe import Recipe

# SET
set_action: bool = False
set_init: bool = False
# GET
get_category: bool = False
get_name: bool = False
get_init: bool = False
# DELETE/UPDATE
modify_recipe: bool = False
# UPDATE
change_photo: bool = False
change_name: bool = False
change_description: bool = False
update_recipe: bool = False
# UTILS
start: bool = True
db_set_transition: bool = False
db_change: bool = False
selecting_recipe: bool = False
#  OTHER
recipe_object: Recipe | None = None
db_con: Connection | None = None
data_array: list[Recipe] = []
data_to_modify: tuple[str, str, str, str | None] | None = None  # (name, recipe_type, desc, photo)
photo_list: list = []


def print_configurations():
    print(
        '# SET\n'
        f'set_action: {set_action}\n'
        f'set_init: {set_init}\n\n'
        '# GET\n'
        f'get_category: {get_category}\n'
        f'get_name: {get_name}\n'
        f'get_init: {get_init}\n\n'
        '# DELETE / UPDATE\n'
        f'modify_recipe: {modify_recipe}\n\n'
        '# UPDATE\n'
        f'change_photo: {change_photo}\n'
        f'change_name: {change_name}\n'
        f'change_description: {change_description}\n'
        f'update_recipe: {update_recipe}\n\n'
        '# UTILS\n'
        f'start: {start}\n'
        f'db_set_trans: {db_set_transition}\n'
        f'db_change: {db_change}\n'
        f'selecting_recipe: {selecting_recipe}\n'
        f'recipe_object: {recipe_object}\n\n'
        '# OTHER\n'
        f'db_con: {db_con}\n'
        f'data_array: {data_array}\n'
        f'transaction_data: {data_to_modify}\n'
        f'photo_list: {photo_list}\n'
    )


# Plugins
nest_asyncio.apply()
load_dotenv()


def int_credentials_getter(creds):
    try:
        return int(creds)
    except TypeError:
        return creds


TOKEN: str = os.getenv('TOKEN')
DASHA_NAME: str = os.getenv('DASHA_USER')
DASHA_ID: int = int_credentials_getter(os.getenv('DASHA_ID'))
IGOR_NAME: str = os.getenv('IGOR_NAME')
IGOR_ID: int = int_credentials_getter(os.getenv('IGOR_ID'))
CLOUD_NAME: str = os.getenv('CLOUD_NAME')
API_KEY: str = os.getenv('API_KEY')
API_SECRET: str = os.getenv('API_SECRET')

cloudinary.config(
    cloud_name=CLOUD_NAME,
    api_key=API_KEY,
    api_secret=API_SECRET
)
