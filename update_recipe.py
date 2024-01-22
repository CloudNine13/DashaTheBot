import utils.config as configurations

from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode


async def update_name(update, context, text):
    context.bot.send_message(
        update.message.chat.id,
        "Окей, новое имя: <i><b>" + text + "</b></i>",
        parse_mode=ParseMode.HTML
    )
    configurations.recipe_object.name = text
    configurations.update_recipe = True
    keyboard = [
        [InlineKeyboardButton("Да", callback_data="Да, описание"),
         InlineKeyboardButton("Нет", callback_data="Нет, описание")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(
        "Меняем описание рецепта? 📋",
        reply_markup=reply_markup
    )


async def update_description(update, context, text):
    context.bot.send_message(
        update.message.chat.id,
        "Хорошо, новое описание выглядит так: <i><b>" + text + "</b></i>",
        parse_mode=ParseMode.HTML
    )
    configurations.recipe_object.description = text
    context.bot.send_message(
        update.message.chat.id,
        "Переходим к изменению рецепта в базе данных..."
    )
    await db.update_item(update.message.chat.id, context.bot)

    # configurations.update_recipe = True
    # reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Да", callback_data="Да, фото"),
    #                                       InlineKeyboardButton("Нет", callback_data="Нет, фото")]])
    # update.message.reply_text(
    #     "Будем менять фото? 📸",
    #     reply_markup=reply_markup
    # )
