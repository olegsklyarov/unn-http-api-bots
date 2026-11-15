from mock import Mock

from bot.dispatcher import Dispatcher
from bot.handlers.persist_update import PersistUpdate
from bot.messenger import Messenger
from bot.storage import Storage
from bot.telegram_messenger import TelegramMessenger


def test_dispatch_persist_update():
    """
    dispatch любого непустого update вызывает storage.persist_update
    с теми же ключами и значениями, что у исходного update.
    """
    update = {
        "update_id": 2026,
        "message": {
            "message_id": 1,
            "from": {"id": 42, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 42, "type": "private"},
            "text": "Hello world",
        },
    }

    persist_update_calls = 0

    def mock_get_user_state(user_id):
        assert user_id == 42
        return {}

    def mock_persist_update(captured_update):
        nonlocal persist_update_calls
        persist_update_calls += 1
        assert captured_update["update_id"] == 2026
        assert captured_update["message"]["message_id"] == 1
        assert captured_update["message"]["from"]["id"] == 42
        assert captured_update["message"]["from"]["is_bot"] is False
        assert captured_update["message"]["from"]["first_name"] == "Test"
        assert captured_update["message"]["chat"]["id"] == 42
        assert captured_update["message"]["chat"]["type"] == "private"
        assert captured_update["message"]["text"] == "Hello world"

    storage: Storage = Mock(
        {
            "get_user_state": mock_get_user_state,
            "persist_update": mock_persist_update,
        }
    )
    # Реальный user_id_from_update, остальные методы Messenger не трогаем (нет HTTP).
    messenger: Messenger = Mock(
        {
            "user_id_from_update": TelegramMessenger().user_id_from_update,
        }
    )

    dispatcher = Dispatcher(storage, messenger)
    dispatcher.add_handlers(PersistUpdate())
    dispatcher.dispatch(update)

    assert persist_update_calls == 1


if __name__ == "__main__":
    test_dispatch_persist_update()
