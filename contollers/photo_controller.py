import uuid

from telegram import Update
from telegram.ext import CallbackContext

import utils.config as configurations


async def photo_controller(update: Update, context: CallbackContext):
    recipe_object = configurations.recipe_object
    if configurations.db_set_trans is True and recipe_object.index == 3:
        img_dir = 'img/' + str(uuid.uuid4()) + '.jpg'
        file = await context.bot.get_file(update.message.photo[-1].file_id)
        await file.download_to_drive(custom_path=img_dir)
        recipe_object.photo_path.append(img_dir)
