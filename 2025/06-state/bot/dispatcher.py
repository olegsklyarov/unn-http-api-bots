import json

from bot.database_client import get_user
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class Dispatcher:
    def __init__(self) -> None:
        self._handlers: list[Handler] = []

    def add_handlers(self, *handlers: Handler) -> None:
        for handler in handlers:
            self._handlers.append(handler)

    def _get_telegram_id_from_update(self, update: dict) -> int:
        """Extract telegram_id from update object."""
        if "message" in update:
            return update["message"]["from"]["id"]
        elif "callback_query" in update:
            return update["callback_query"]["from"]["id"]
        return None

    def dispatch(self, update: dict) -> None:
        # Get user state for handlers that need it
        telegram_id = self._get_telegram_id_from_update(update)
        user = get_user(telegram_id) if telegram_id else None

        user_state = user.get("state") if user else None

        user_data = user["data"] if user else "{}"
        if user_data is None:
            user_data = "{}"
        order_data = json.loads(user_data)

        for handler in self._handlers:
            if handler.can_handle(update, user_state, order_data):
                if handler.handle(update, user_state, order_data) == HandlerStatus.STOP:
                    break
