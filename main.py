from telegram import Update
from telegram.ext import filters, ContextTypes
from utils.config import TOKEN
from handlers.button_handler import button_handler
from handlers.error_handler import error_handler
from handlers.message_handler import set_message_command, get_message_command, message_handler
from handlers.image_handler import image_handler
from start import start
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler


async def bad_command_mock(_, context: ContextTypes.DEFAULT_TYPE) -> None:
    await context.bot.mock_function()


def main():
    application = Application.builder().token(TOKEN).build()

    command_start = CommandHandler(command='start', callback=start)
    command_get = CommandHandler(command='get', callback=get_message_command)
    command_set = CommandHandler(command='set', callback=set_message_command)
    bad_command = CommandHandler(command='bad', callback=bad_command_mock)

    application.add_error_handler(error_handler)

    application.add_handler(command_start)
    application.add_handler(command_get)
    application.add_handler(command_set)
    application.add_handler(bad_command)

    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.PHOTO & (~ filters.TEXT), image_handler))
    application.add_handler(MessageHandler(filters.TEXT & (~ filters.PHOTO), message_handler))

    application.run_polling()


if __name__ == '__main__':
    main()
