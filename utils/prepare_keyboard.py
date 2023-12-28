from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from server.fetchactions.fetch_categories import fetch_categories


def prepare_keyboard():
    keyboard = []
    for row in fetch_categories():
        keyboard.append([InlineKeyboardButton(row[0], callback_data=str(row[0]) + str(row[2]))])
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup
