import utils.config as configurations
from models.recipe import Recipe


def clear_configurations():
    # SET
    configurations.set_action = False
    configurations.set_init = False
    # GET
    configurations.get_category = False
    configurations.get_name = False
    configurations.get_init = False
    # DELETE/UPDATE
    configurations.can_change = False
    # UPDATE
    configurations.change_photo = False
    configurations.change_name = False
    configurations.change_description = False
    configurations.update_recipe = False
    # UTILS
    configurations.start = True
    configurations.db_set_trans = False
    configurations.db_change = False
    configurations.recipe_type = False
    #  OTHER
    configurations.recipe_object = Recipe()
    configurations.db_con = None
    configurations.data_array = []
    configurations.transaction_data = None
