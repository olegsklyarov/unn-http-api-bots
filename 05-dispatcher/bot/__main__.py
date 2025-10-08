import bot.long_polling
from bot.dispatcher import Dispatcher
from bot.handlers.message_echo import MessageEcho
from bot.handlers.update_database_logger import UpdateDatabaseLogger


def main() -> None:
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handler(UpdateDatabaseLogger())
        dispatcher.add_handler(MessageEcho())

        bot.long_polling.start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
