from bot import long_polling
from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers
from bot.messenger import Messenger
from bot.storage import Storage
from bot.telegram_bot_api import TelegramMessenger
from bot.users_storage import JsonUsersStorage


def main() -> None:
    try:
        storage: Storage = JsonUsersStorage()
        messenger: Messenger = TelegramMessenger()
        dispatcher = Dispatcher(storage, messenger)
        dispatcher.add_handlers(*get_handlers())
        long_polling.start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
