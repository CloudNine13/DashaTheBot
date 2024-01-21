import logging

from pydoc import html
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)

logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CallbackContext):
    logger.error("Exception while handling an update:", exc_info=context.error)
    message = (
        "<pre>Произошла ошибка! "
        "Обратитесь к Игорю!</pre>\n"
        f"<pre>context.error = {html.escape(str(context.error))}</pre>\n"
        f"<pre>update.effective_chat = {html.escape(str(update.effective_chat))}</pre>\n\n"
        f"<pre>update.effective_user = {html.escape(str(update.effective_user))}</pre>\n\n"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message, parse_mode=ParseMode.HTML)
