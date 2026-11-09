import json

from bot import telegram_bot_api
from bot.dispatcher import Dispatcher


def start_long_polling(dispatcher: Dispatcher) -> None:
    next_update_offset = 0
    while True:
        updates = telegram_bot_api.get_updates(
            offset=next_update_offset,
            timeout=30,
            # Иначе остаётся прошлый allowed_updates (например только message) —
            # callback_query не приходит, inline-кнопки «не работают».
            allowed_updates=json.dumps(["message", "callback_query"]),
        )
        for update in updates:
            next_update_offset = max(next_update_offset, update["update_id"] + 1)
            dispatcher.dispatch(update)
            print(".", end="", flush=True)
