import db
import utils.config as configurations

from telegram.ext import CallbackContext
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.constants import ParseMode
from server.setactions.set_recipe import set_recipe
from utils.randomizer import random_heart, random_emoji
from utils.clear_config import clear_configurations
from utils.prepare_keyboard import prepare_keyboard
from models.recipe import Recipe
from set_recipe import ask_subcategory, set_new_recipe
from get_recipe import get_category_item, get_all


async def button_controller(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    choice = query.data

    if configurations.set_init is True or configurations.get_category is True:
        await context.bot.send_message(
            update.callback_query.message.chat.id,
            f'Вы выбрали: <i><b>{choice[:-1]}</b></i> {random_emoji()}',
            parse_mode=ParseMode.HTML
        )
        if choice[-1] == '1':
            await ask_subcategory(update, choice[:-1])

        elif choice[-1] == '0':
            if configurations.set_init is True:
                configurations.set_init = False  # Set init off
                await set_new_recipe(update, context, recipe_type=choice[:-1])
            elif configurations.get_category is True:
                configurations.get_category = False
                await get_category_item(update, context, recipe_type=choice[:-1])

    elif configurations.set_action is True:
        if configurations.change_photo:
            configurations.db_change = True

        configurations.db_set_transition = True
        configurations.set_action = False
        configurations.change_photo = False
        recipe_object = configurations.recipe_object

        if choice == 'да':
            recipe_object.index += 1
            keyboard = [[KeyboardButton(text='готово')]]
            reply_markup = ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True)
            await update.callback_query.message.reply_text(
                'Жду изображений! Пожалуйста, после загрузки медиа, нажмите готово, чтобы '
                'подтвердить сохранение картинок. Документы, не относящиеся к картинкам или'
                f'фотографиям, не будут обработаны (ограничение телеграмм бота 😞). Спасибо {random_heart()}!',
                reply_markup=reply_markup
            )

        elif choice == 'нет':
            recipe_object.index += 1
            recipe_object.photo_path = []
            assert recipe_object.index == recipe_object.max_index
            await context.bot.send_message(
                update.callback_query.message.chat.id,
                f'Ну что же! Переходим к сохранению рецепта! Спасибо {random_heart()}'
            )
            if configurations.db_set_transition:
                await set_recipe(update.callback_query.message.chat.id, context.bot)
            elif configurations.db_change:
                await db.update_item(update.callback_query.message.chat.id, context.bot)

    elif configurations.get_init is True:
        configurations.get_init = False
        await context.bot.send_message(
            update.callback_query.message.chat.id,
            f'Хорошо, будем искать <i><b>{choice}</b></i> ',
            parse_mode=ParseMode.HTML
        )

        if choice == 'имя':
            configurations.get_name = True
            await context.bot.send_message(
                update.callback_query.message.chat.id,
                'Укажите точное название рецепта 📖',
            )

        elif choice == 'категорию':
            configurations.get_category = True
            reply_markup = prepare_keyboard()
            await update.callback_query.message.reply_text(
                'Выберите нужную категорию 📋',
                reply_markup=reply_markup
            )

        elif choice == 'все':
            configurations.get_all = True
            await get_all(update, context)

    elif configurations.can_change is True and configurations.transaction_data is not None:
        configurations.can_change = False

        if choice == 'удалить':
            await db.delete_item(update.callback_query.message.chat.id, context.bot)
            await context.bot.send_message(
                update.callback_query.message.chat.id,
                f'Рецепт удалён! Не забудьте обязательно добавить новый! {random_heart()}'
            )
            clear_configurations()

        elif choice == 'изменить':
            configurations.update_recipe = True
            configurations.recipe_object = Recipe()
            configurations.recipe_object.name = configurations.transaction_data[0]
            configurations.recipe_object.recipe_type = configurations.transaction_data[1]
            configurations.recipe_object.description = configurations.transaction_data[2]
            configurations.recipe_object.photo_path = configurations.transaction_data[3]
            keyboard = [
                [InlineKeyboardButton('Да', callback_data='Да, имя'),
                 InlineKeyboardButton('Нет', callback_data='Нет, имя')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.message.reply_text(
                'Вы будете менять имя рецепта? 📖',
                reply_markup=reply_markup
            )

    elif configurations.update_recipe is True:
        configurations.update_recipe = False

        if choice == 'Да, имя':
            configurations.change_name = True
            await context.bot.send_message(
                update.callback_query.message.chat.id,
                'Введите новое название рецепта'
            )

        if choice == 'Нет, имя':
            configurations.update_recipe = True
            keyboard = [
                [InlineKeyboardButton('Да', callback_data='Да, описание'),
                 InlineKeyboardButton('Нет', callback_data='Нет, описание')]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.callback_query.message.reply_text(
                'Меняем описание рецепта? 📋',
                reply_markup=reply_markup
            )

        if choice == 'Да, описание':
            configurations.change_description = True
            await context.bot.send_message(
                update.callback_query.message.chat.id,
                'Введите новое описание рецепта'
            )

        if choice == 'Нет, описание':
            configurations.update_recipe = False
            await context.bot.send_message(
                update.callback_query.message.chat.id,
                'Отлично! Переходим к изменению рецепта в базе данных...'
            )
            await db.update_item(update.callback_query.message.chat.id, context.bot)

            # configurations.update_recipe = True
            # keyboard = [
            #     [InlineKeyboardButton('Да', callback_data='Да, фото'),
            #      InlineKeyboardButton('Нет', callback_data='Нет, фото')]
            # ]
            # reply_markup = InlineKeyboardMarkup(keyboard)
            # update.callback_query.message.reply_text(
            #     'Меняем фото? 📸',
            #     reply_markup=reply_markup
            # )

        # if choice == 'Да, фото':
        #     configurations.db_change = True
        #     recipe_object = configurations.recipe_object
        #     recipe_object.index += 1
        #     context.bot.send_message(
        #         update.callback_query.message.chat.id,
        #         'Жду изображений! Пожалуйста, после загрузки медиа, напишите готово, '
        #         'чтобы подтвердить сохранение картинок. Спасибо ' + helper.random_heart()
        #     )
        #
        # if choice == 'Нет, фото':
        #     configurations.update_recipe = False
        #     context.bot.send_message(
        #         update.callback_query.message.chat.id,
        #         'Отлично! Переходим к изменению рецепта в базе данных...'
        #     )
        #     db.update_item(update.callback_query.message.chat.id, context.bot)
