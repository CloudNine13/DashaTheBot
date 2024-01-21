import uuid
import utils.config as configurations

from telegram import Update
from telegram.ext import CallbackContext


async def photo_controller(update: Update, context: CallbackContext):
    recipe_object = configurations.recipe_object
    if configurations.db_set_transition is True and recipe_object.index == 3:
        image_id = str(uuid.uuid4())
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        file_bytes = await file.download_as_bytearray()
        recipe_object.photo_path.append(image_id)
        configurations.photo_list.append({'file': file_bytes, 'public_id': image_id})
