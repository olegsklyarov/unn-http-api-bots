from bot import users_storage
from bot.handler import Handler
from bot.handler import HandlerStatus


class Dispatcher:
    def __init__(self) -> None:
        self._handlers: list[Handler] = []

    def add_handlers(self, *handlers: Handler) -> None:
        for handler in handlers:
            self._handlers.append(handler)

    def dispatch(self, update: dict) -> None:
        user_id = users_storage.user_id_from_update(update)
        if user_id is None:
            return
        state = users_storage.get_user_state(user_id)
        for handler in self._handlers:
            if handler.can_handle(update, state):
                if handler.handle(update, state) == HandlerStatus.STOP:
                    break
