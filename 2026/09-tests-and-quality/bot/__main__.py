from bot import long_polling
from bot.dispatcher import Dispatcher
from bot.files_storage import JsonFilesStorage
from bot.handlers import get_handlers
from bot.messenger import Messenger
from bot.storage import Storage
from bot.telegram_messenger import TelegramMessenger


def main() -> None:
    try:
        storage: Storage = JsonFilesStorage()
        messenger: Messenger = TelegramMessenger()
        dispatcher = Dispatcher(storage, messenger)
        dispatcher.add_handlers(*get_handlers())
        long_polling.start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
