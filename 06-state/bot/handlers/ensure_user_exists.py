from bot.database_client import ensure_user_exists
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class EnsureUserExists(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        # This handler should run for any update that has a user ID
        return "message" in update and "from" in update["message"]

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        # Ensure user exists (check and create if needed in single transaction)
        ensure_user_exists(telegram_id)

        # Continue processing with other handlers
        return HandlerStatus.CONTINUE
