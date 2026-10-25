"""Точка входа: собираем Dispatcher и запускаем long polling.

Composition root — здесь только сборка, не обработка updates.
Open–closed: новый сценарий = новый Handler в get_handlers(), без правки Dispatcher.
https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle
См. ../README.md (шаг 10), ../ARCHITECTURE.md
"""

from bot import long_polling
from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers


def main() -> None:
    try:
        dispatcher = Dispatcher()
        dispatcher.add_handlers(*get_handlers())
        long_polling.start_long_polling(dispatcher)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
