import utils.config as configurations

from utils.photo_string import make_photo_string


def prepare_recipe_object():
    configurations.set_action = False
    recipe_object = configurations.recipe_object
    if recipe_object.photo_path:
        # ['1', '2', '3'] => "1, 2, 3"
        photo_string = make_photo_string(recipe_object.photo_path)
    else:
        photo_string = None
    recipe_object.photo_path = photo_string
    return recipe_object
