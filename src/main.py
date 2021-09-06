import logging
import os
import threading
from abc import ABC, abstractmethod

from dotenv import load_dotenv, find_dotenv
from telegram import ReplyKeyboardMarkup, KeyboardButton, Update, ReplyKeyboardRemove
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler


def configure_logging() -> logging:
    """This is the method to configure logger.
    :return logging: return configured logger object"""

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    return logging.getLogger(__name__)


logger = configure_logging()
load_dotenv(find_dotenv())
TOKEN = os.environ["BOT_TOKEN"]


class ApplicationAbstractClass(ABC):

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def setup(self):
        pass

    @abstractmethod
    def start_menu(self, update: Update, context: CallbackContext) -> None:
        pass

    @abstractmethod
    def data_controller(self):
        pass

    @abstractmethod
    def button_controller(self):
        pass


class CustomApplication(ApplicationAbstractClass):

    updater: Updater

    def start(self):
        print("start: Starting to poll...")
        self.updater.start_polling()
        self.updater.idle()

    def setup(self):
        self.updater = Updater(TOKEN, use_context=True, request_kwargs={'read_timeout': 1000, 'connect_timeout': 1000})
        dp = self.updater.dispatcher
        start_handler = CommandHandler("start", self.start_menu)
        controller_handler = MessageHandler(Filters.text, self.data_controller)
        dp.add_handler(start_handler)
        dp.add_handler(controller_handler)
        dp.add_handler(CallbackQueryHandler(self.button_controller))
        print("setup_dispatcher: Dispatcher is successfully configured!")
        self.start()

    def start_menu(self, update: Update, context: CallbackContext) -> None:
        main_menu_keyboard = [
            [KeyboardButton(text="Посмотреть рецепт \U0001F372")],
            [KeyboardButton(text="Добавить рецепт \u270D")]
        ]
        main_menu = ReplyKeyboardMarkup(main_menu_keyboard)
        um = update.message
        um.reply_text(text="Вас приветствует книга рецептов DashaCooking!")
        um.reply_text(text="Выберите действие", reply_markup=main_menu)

    def data_controller(self):
        pass

    def button_controller(self):
        pass


if __name__ == '__main__':
    CustomApplication().setup()
