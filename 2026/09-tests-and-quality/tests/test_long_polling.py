from mock import Mock

from bot.dispatcher import Dispatcher
from bot.long_polling import start_long_polling
from bot.messenger import Messenger


def test_single_update_dispatches_and_advances_offset():
    """
    Happy-path start_long_polling через Mock messenger и dispatcher.

    Проверяем:
    1. Первый get_updates вызывается с offset=0, limit=10, timeout=30 и
       allowed_updates='["message", "callback_query"]'.
    2. Мок messenger возвращает список из одного update:
       update_id=2026, текстовое сообщение "Hello world".
    3. На dispatcher вызывается dispatch с тем же update (по содержимому).
    4. Второй get_updates уже с offset=2027 (update_id + 1).
    5. Цикл останавливается исключением KeyboardInterrupt.
    """
    mock_update_1 = {
        "update_id": 2026,
        "message": {
            "message_id": 1,
            "from": {"id": 1, "is_bot": False, "first_name": "Test"},
            "chat": {"id": 1, "type": "private"},
            "text": "Hello world",
        },
    }

    get_updates_calls_count = 0
    dispatched = []

    def mock_get_updates(**params):
        """Обслуживает два вызова get_updates в цикле long polling."""
        nonlocal get_updates_calls_count
        get_updates_calls_count += 1
        if get_updates_calls_count == 1:
            # Первый вызов: стартовый offset и параметры long polling
            assert params["offset"] == 0
            assert params["limit"] == 10
            assert params["timeout"] == 30
            assert params["allowed_updates"] == '["message", "callback_query"]'
            return [mock_update_1]
        # Второй вызов: offset сдвинут на update_id + 1; останавливаем цикл
        assert params["offset"] == 2027
        raise KeyboardInterrupt

    def mock_dispatch(update):
        assert update["update_id"] == 2026
        assert update["message"]["message_id"] == 1
        assert update["message"]["from"]["id"] == 1
        assert update["message"]["from"]["is_bot"] is False
        assert update["message"]["from"]["first_name"] == "Test"
        assert update["message"]["chat"]["id"] == 1
        assert update["message"]["chat"]["type"] == "private"
        assert update["message"]["text"] == "Hello world"
        dispatched.append(update)

    messenger: Messenger = Mock({"get_updates": mock_get_updates})
    dispatcher: Dispatcher = Mock({"dispatch": mock_dispatch})

    try:
        start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        pass

    assert get_updates_calls_count == 2
    assert dispatched == [mock_update_1]


def test_empty_updates_does_not_dispatch():
    """Пустой updates: dispatch не вызывается, offset остаётся 0."""
    get_updates_calls_count = 0
    dispatched = []

    def mock_get_updates(**params):
        nonlocal get_updates_calls_count
        get_updates_calls_count += 1
        if get_updates_calls_count == 1:
            assert params["offset"] == 0
            return []
        assert params["offset"] == 0
        raise KeyboardInterrupt

    def mock_dispatch(update):
        dispatched.append(update)

    messenger: Messenger = Mock({"get_updates": mock_get_updates})
    dispatcher: Dispatcher = Mock({"dispatch": mock_dispatch})

    try:
        start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        pass

    assert get_updates_calls_count == 2
    assert dispatched == []


def test_unordered_update_ids_uses_max_offset():
    """Два update с неупорядоченными update_id: следующий offset = max(id) + 1."""
    get_updates_calls_count = 0
    dispatched = []

    # Сначала больший id, потом меньший — без max offset стал бы 51.
    update_high = {"update_id": 100, "message": {"text": "first"}}
    update_low = {"update_id": 50, "message": {"text": "second"}}

    def mock_get_updates(**params):
        nonlocal get_updates_calls_count
        get_updates_calls_count += 1
        if get_updates_calls_count == 1:
            assert params["offset"] == 0
            return [update_high, update_low]
        assert params["offset"] == 101
        raise KeyboardInterrupt

    def mock_dispatch(update):
        dispatched.append(update)

    messenger: Messenger = Mock({"get_updates": mock_get_updates})
    dispatcher: Dispatcher = Mock({"dispatch": mock_dispatch})

    try:
        start_long_polling(dispatcher, messenger)
    except KeyboardInterrupt:
        pass

    assert get_updates_calls_count == 2
    assert dispatched == [update_high, update_low]


if __name__ == "__main__":
    test_single_update_dispatches_and_advances_offset()
    test_empty_updates_does_not_dispatch()
    test_unordered_update_ids_uses_max_offset()
