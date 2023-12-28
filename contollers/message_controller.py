from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode

import db
import utils.config as configurations

from utils.clear_config import clear_configurations
from set_recipe import _set_init
from get_recipe import get_name, get_item

from update_recipe import update_name, update_description


async def set_message_command(update: Update, context: CallbackContext):
    configurations.start = True  # Start on
    clear_configurations()
    await message_controller(update, context)


async def get_message_command(update: Update, context: CallbackContext):
    configurations.start = True  # Start on
    clear_configurations()
    await message_controller(update, context)


async def message_controller(update: Update, context: CallbackContext):
    text: str | None = update.message.text

    if configurations.start is True:
        configurations.start = False  # Start off
        if text == 'Посмотреть рецепт\U0001F967' or text == '/get':
            configurations.get_init = True
            keyboard = [
                [InlineKeyboardButton('По имени', callback_data='имя'),
                 InlineKeyboardButton('По категории', callback_data='категорию')],
                [InlineKeyboardButton('Показать всё', callback_data='все')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                'Как будем искать? 👀',
                reply_markup=reply_markup
            )

        elif text == 'Добавить рецепт\U0001f50e' or text == '/set':
            await _set_init(update, context)

        elif text == 'База данных':
            database = open('recipes.db', 'rb')
            await context.bot.send_document(chat_id=update.message.chat_id, document=database)
            database.close()

    elif configurations.set_action is True:
        recipe_object = configurations.recipe_object
        if recipe_object.index == 0:
            recipe_object.index += 1
            recipe_object.name = text
            await context.bot.send_message(
                update.message.chat.id,
                'Вы указали имя: <i><b>' + text + '</b></i>',
                parse_mode=ParseMode.HTML
            )
            await context.bot.send_message(
                update.message.chat.id,
                'Пожалуйста, добавьте описание 📙'
            )

        elif recipe_object.index == 1:
            print('recipe_object.index += 1', recipe_object)
            recipe_object.index += 1
            recipe_object.description = text
            await context.bot.send_message(
                update.message.chat.id,
                'О рецепте нам известно следующее: <i><b>' + text + '</b></i>',
                parse_mode=ParseMode.HTML
            )
            keyboard = [
                [InlineKeyboardButton('Да', callback_data='да'), InlineKeyboardButton('Нет', callback_data='нет')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text(
                'Добавим фотографию или скриншот? 📸',
                reply_markup=reply_markup
            )

    elif configurations.db_set_trans is True or configurations.db_change is True:
        if text.lower() == 'готово':

            if configurations.db_set_trans:
                configurations.db_set_trans = False
                await db.save_recipe(update.message.chat.id, context.bot)

            elif configurations.db_change:
                configurations.db_change = False
                await db.update_item(update.message.chat.id, context.bot)

    elif configurations.get_name is True:
        configurations.get_name = False
        await context.bot.send_message(
            update.message.chat.id,
            'Всё понял, ищем <i><b>' + text + '</b></i>',
            parse_mode=ParseMode.HTML
        )
        await get_name(update, context, text)

    elif configurations.recipe_type is True:
        try:
            print('config.data_array', configurations.data_array)
            print('int(text)', int(text))
            print('config.data_array[int(text) - 1]', configurations.data_array[int(text) - 1])

            await get_item(update, context, configurations.data_array[int(text) - 1])
            configurations.recipe_type = False
        except ValueError:
            await context.bot.send_message(
                update.message.chat.id,
                'Пожалуйста, выберите <ins><i><b>ЦИФРУ</b></i></ins>',
                parse_mode=ParseMode.HTML
            )
        except IndexError:
            await context.bot.send_message(
                update.message.chat.id,
                'Такого номера нет. Выберите существующий.',
                parse_mode=ParseMode.HTML
            )

    elif configurations.change_name is True:
        configurations.change_name = False
        await update_name(update, context, text)

    elif configurations.change_description is True:
        configurations.change_description = False
        await update_description(update, context, text)
