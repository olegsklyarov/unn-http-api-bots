import bot.long_polling
from bot.dispatcher import Dispatcher
from bot.handlers.callback_cancel import CallbackCancel
from bot.handlers.message_button_inline import MessageButtonInline
from bot.handlers.message_start import MessageStart
from bot.handlers.update_database_logger import UpdateDatabaseLogger


def main() -> None:
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handler(UpdateDatabaseLogger())
        dispatcher.add_handler(MessageStart())
        dispatcher.add_handler(MessageButtonInline())
        dispatcher.add_handler(CallbackCancel())
        # dispatcher.add_handler(MessageEcho())

        bot.long_polling.start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
