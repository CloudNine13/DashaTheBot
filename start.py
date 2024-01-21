from telegram import KeyboardButton, ReplyKeyboardMarkup, Update, Message

import utils.config as conf
from utils.check_user import check_developer
from utils.clear_config import clear_configurations
from utils.randomizer import random_heart


async def start(update: Update, _):
    clear_configurations()

    send_database_button = []

    if check_developer(update.effective_user.username, update.effective_user.id):
        send_database_button = [KeyboardButton(text="База данных 📓")]

    main_menu_keyboard = [[KeyboardButton(text="Посмотреть рецепт\U0001F967")],
                          [KeyboardButton(text="Добавить рецепт\U0001f50e")], send_database_button]

    main_menu = ReplyKeyboardMarkup(keyboard=main_menu_keyboard, resize_keyboard=True, one_time_keyboard=True)

    um: Message = update.message

    await um.reply_text(text=f"Добро пожаловать! Это бот для рецептов, принадлежащий Дашульке! {random_heart()}")
    await um.reply_text(text="Что бы вы хотели сделать?", reply_markup=main_menu)
