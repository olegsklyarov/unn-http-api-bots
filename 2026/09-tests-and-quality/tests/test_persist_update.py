import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import bot.handlers.persist_update as persist_update_handler
from bot.dispatcher import Dispatcher
from bot.handlers import get_handlers
from bot.long_polling import start_long_polling


class Mock:
    def __init__(self, dictionary: dict) -> None:
        for k, v in dictionary.items():
            setattr(self, k, v)


update = {
    "update_id": 1,
    "message": {
        "message_id": 10,
        "from": {"id": 42, "is_bot": False, "first_name": "Test"},
        "chat": {"id": 42, "type": "private"},
        "text": "hello",
    },
}

get_updates_calls = {"count": 0}


def get_updates(**params):
    get_updates_calls["count"] += 1
    if get_updates_calls["count"] == 1:
        return [update]
    raise KeyboardInterrupt


def user_id_from_update(received_update):
    return received_update["message"]["from"]["id"]


def get_user_state(user_id):
    return {
        "current_state": "waiting_for_recipe",
        "order_content": {
            "recipe": None,
            "size": None,
            "crust": None,
            "drink": None,
        },
    }


def persist_user(received_update):
    pass


def persist_update(received):
    persist_update.called = True
    assert received is update


persist_update.called = False
persist_update_handler.updated_logger = Mock({
    "persist_update": persist_update
})

messenger = Mock(
    {
        "get_updates": get_updates,
        "user_id_from_update": user_id_from_update,
    }
)
storage = Mock(
    {
        "get_user_state": get_user_state,
        "persist_user": persist_user,
    }
)

dispatcher = Dispatcher(storage, messenger)
dispatcher.add_handlers(*get_handlers())

try:
    start_long_polling(dispatcher, messenger)
except KeyboardInterrupt:
    pass

assert persist_update.called
