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
