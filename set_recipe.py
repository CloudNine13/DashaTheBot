import utils.config as configurations

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import CallbackContext
from server.fetchactions.fetch_subcategory import fetch_subcategory
from utils.check_user import check_user
from utils.prepare_keyboard import prepare_keyboard
from utils.clear_config import clear_configurations
from models.recipe import Recipe


async def _set_init(update: Update, context: CallbackContext):
    configurations.set_init = True  # Set init on
    reply_markup = prepare_keyboard()
    await context.bot.send_message(update.message.chat_id, "Добрый день! ☀️")

    if check_user(update.effective_user.username, update.effective_user.id):
        await update.message.reply_text("Какой рецепт вы хотите добавить?", reply_markup=reply_markup)

    else:
        clear_configurations()
        configurations.start = True
        await update.message.reply_text("Добалять рецепты могут только Игорь и Даша 😞")


async def ask_subcategory(update: Update, recipe_type):
    keyboard = []
    for row in fetch_subcategory(recipe_type):
        keyboard.append([InlineKeyboardButton(row[0], callback_data=str(row[0]) + str(row[2]))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_text("Уточните категорию", reply_markup=reply_markup)


async def set_new_recipe(update: Update, context: CallbackContext, recipe_type):
    configurations.set_action = True
    recipe = Recipe()
    recipe.recipe_type = recipe_type
    configurations.recipe_object = recipe
    await context.bot.send_message(update.callback_query.message.chat_id, "Отлично! Укажите имя будущего рецепта 🍽️")
