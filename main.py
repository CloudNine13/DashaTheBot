from telegram.ext import filters
from utils.config import TOKEN
from contollers.button_controller import button_controller
from contollers.error_controller import error_handler
from contollers.message_controller import set_message_command, get_message_command, message_controller
from contollers.photo_controller import photo_controller
from start import start
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler


def main():
    application = Application.builder().token(TOKEN).build()

    command_start = CommandHandler(command='start', callback=start, block=False)
    command_get = CommandHandler(command='get', callback=get_message_command, block=False)
    command_set = CommandHandler(command='set', callback=set_message_command, block=False)

    application.add_error_handler(error_handler)

    application.add_handler(command_start)
    application.add_handler(command_get)
    application.add_handler(command_set)

    application.add_handler(CallbackQueryHandler(button_controller, block=False))
    application.add_handler(MessageHandler(filters.PHOTO & (~ filters.TEXT), photo_controller, block=False))
    application.add_handler(MessageHandler(filters.TEXT & (~ filters.PHOTO), message_controller, block=False))

    application.run_polling()


if __name__ == '__main__':
    main()
