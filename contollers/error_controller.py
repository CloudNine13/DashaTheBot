import logging

from pydoc import html

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes, CallbackContext

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)

logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CallbackContext):
    logger.error("Exception while handling an update:", exc_info=context.error)
    message = (
        f"<pre>Произошла ошибка!""</pre>\n"
        f"<pre>context.chat_data = {html.escape(str(context.chat_data))}</pre>\n\n"
        f"<pre>context.user_data = {html.escape(str(context.user_data))}</pre>\n\n"
        f"<pre>Обратитесь к Игорю!</pre>"
    )
    await context.bot.send_message(chat_id=update.effective_message.chat.id,
                                   text=message, parse_mode=ParseMode.HTML)
