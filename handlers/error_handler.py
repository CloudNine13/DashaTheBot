import utils.config as configurations
import json
import logging
import traceback
import html

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CallbackContext

logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.ERROR)

logger = logging.getLogger(__name__)


async def error_handler(update: Update, context: CallbackContext):
    logger.error("Exception while handling an update:", exc_info=context.error)
    tb_list = traceback.format_exception(None, context.error, context.error.__traceback__)
    tb_string = "".join(tb_list)
    update_str = update.to_dict() if isinstance(update, Update) else str(update)
    message_user = "🚨Произошла ошибка! Обратитесь к Игорю!🚨"
    message_developer = (
        f"<pre>update = {html.escape(json.dumps(update_str, indent=2, ensure_ascii=False))}</pre>\n"
        f"<pre>context.error = {html.escape(str(context.error))}</pre>\n"
        f"<pre>{html.escape(tb_string)}</pre>"
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=message_user, parse_mode=ParseMode.HTML)
    await context.bot.send_message(chat_id=configurations.IGOR_ID, text=message_developer, parse_mode=ParseMode.HTML)
