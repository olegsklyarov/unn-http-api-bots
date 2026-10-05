from bot.handler import Handler
from bot.handler_result import HandlerStatus


class Dispatcher:
    def __init__(self) -> None:
        self._handlers: list[Handler] = []

    def add_handlers(self, *handlers: Handler) -> None:
        for handler in handlers:
            self._handlers.append(handler)

    def dispatch(self, update: dict) -> None:
        for handler in self._handlers:
            if handler.can_handle(update):
                if handler.handle(update) == HandlerStatus.STOP:
                    break
