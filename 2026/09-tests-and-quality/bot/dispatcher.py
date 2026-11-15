from bot.handler import Handler
from bot.handler import HandlerStatus
from bot.messenger import Messenger
from bot.storage import Storage


class Dispatcher:
    def __init__(self, storage: Storage, messenger: Messenger) -> None:
        self._storage = storage
        self._messenger = messenger
        self._handlers: list[Handler] = []

    def add_handlers(self, *handlers: Handler) -> None:
        for handler in handlers:
            self._handlers.append(handler)

    def dispatch(self, update: dict) -> None:
        user_id = self._messenger.user_id_from_update(update)
        if user_id is None:
            return
        state = self._storage.get_user_state(user_id)
        for handler in self._handlers:
            if handler.can_handle(update, state, self._storage, self._messenger):
                if handler.handle(update, state, self._storage, self._messenger) == HandlerStatus.STOP:
                    break
