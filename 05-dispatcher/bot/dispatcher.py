from bot.handler import Handler
from bot.handler_result import HandlerStatus


class Dispatcher:
    def __init__(self) -> None:
        self.handlers: list[Handler] = []

    def add_handler(self, handler: Handler) -> None:
        self.handlers.append(handler)

    def dispatch(self, update: dict) -> None:
        for handler in self.handlers:
            if handler.can_handle(update):
                if handler.handle(update) == HandlerStatus.STOP:
                    break
