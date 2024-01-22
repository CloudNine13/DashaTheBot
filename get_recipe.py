import utils.config as configurations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext
from server.fetchactions.fetch_recipe_by_name import fetch_recipe_by_name
from utils.check_user import check_user
from server.fetchactions.fetch_category_item import fetch_category_items
from server.fetchactions.fetch_all_recipes import fetch_all_recipes as fetch_all_recipes
from utils.clear_config import clear_configurations
from utils.images.download_images import download_images


async def get_category_item(update: Update, context: CallbackContext, recipe_type):
    index = 0
    info_string = ''
    for row in fetch_category_items(recipe_type) or []:
        index += 1
        configurations.data_array.append(row)
        info_string += f'{index}. <b>{row[0]}</b>, (<i>{row[1]}</i>)\n'
    await update.effective_message.reply_text("Вот что мы имеем в итоге:")
    if index == 0:
        configurations.start = True
        info_string = 'Ничего не найдено! Уточните название или <u>добавьте новый рецепт</u>!'
        await context.bot.send_message(update.effective_chat.id, info_string, parse_mode=ParseMode.HTML)
    else:
        configurations.selecting_recipe = True
        await context.bot.send_message(update.effective_chat.id, info_string, parse_mode=ParseMode.HTML)
        await update.effective_message.reply_text("Введите цифру интересующего вас рецепта")


async def get_name(update: Update, context: CallbackContext, name: str):
    index = 0
    info_string = ''

    for recipe_name in fetch_recipe_by_name(name) or []:
        index += 1
        configurations.data_array.append(recipe_name)
        info_string += f'{index}. <b>{recipe_name[0]}</b>, (<i>{recipe_name[1]}</i>)\n'

    await update.message.reply_text("Вот что мы имеем в итоге:")

    if index == 0:
        configurations.start = True
        info_string = 'Ничего не найдено! Уточните название или <u>добавьте новый рецепт</u>!'
        await context.bot.send_message(update.effective_chat.id, info_string, parse_mode=ParseMode.HTML)
    else:
        configurations.selecting_recipe = True
        await context.bot.send_message(update.effective_chat.id, info_string, parse_mode=ParseMode.HTML)
        await update.effective_message.reply_text("Введите цифру интересующего вас рецепта")


async def get_all(update: Update, context: CallbackContext):
    index = 0
    info_string = ''
    recipes = fetch_all_recipes()

    for recipe in recipes:
        index += 1
        configurations.data_array.append(recipe)
        info_string += f'{index}. <b>{recipe[0]}</b>, (<i>{recipe[1]}</i>)\n'

    await update.effective_message.reply_text("Вот что мы имеем в итоге:")

    if index == 0:
        configurations.start = True
        info_string = 'Ничего не найдено! Уточните название или <u>добавьте новый рецепт</u>!'
        await context.bot.send_message(update.effective_chat.id, info_string, parse_mode=ParseMode.HTML)

    else:
        configurations.selecting_recipe = True
        await context.bot.send_message(update.effective_chat.id, info_string, parse_mode=ParseMode.HTML)
        await update.effective_message.reply_text("Введите цифру интересующего вас рецепта")


async def get_item(update: Update, context: CallbackContext, item):
    string = f"Название: <b>{item[0]}</b> \nКатегория: <i>{item[1]}</i> \n\nОписание: {item[2]}"
    await context.bot.send_message(update.message.chat.id, string, parse_mode=ParseMode.HTML)

    if item[3] != 'NULL' and item[3] != 'None' and item[3] is not None:
        image_list = download_images(item[3])
        if image_list[0]:  # Bytearray can be empty
            await context.bot.send_media_group(chat_id=update.message.chat.id, media=image_list)

    if check_user(name=update.effective_user.username, user_id=update.effective_user.id):
        configurations.selecting_recipe = False
        configurations.data_array = []
        configurations.data_to_modify = item
        configurations.modify_recipe = True

        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(text="Удалить рецепт ❌", callback_data="удалить")],
                                             [InlineKeyboardButton(text="Изменить рецепт ⚠️", callback_data="изменить")]
                                             ])
        await update.message.reply_text("⚙️ Опции:", reply_markup=reply_markup)

    else:
        clear_configurations()
