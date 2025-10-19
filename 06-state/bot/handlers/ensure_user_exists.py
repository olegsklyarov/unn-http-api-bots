from bot.database_client import user_exists, create_user
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class EnsureUserExists(Handler):
    def can_handle(self, update: dict) -> bool:
        # This handler should run for any update that has a user ID
        return "message" in update and "from" in update["message"]

    def handle(self, update: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        # Check if user exists, if not create them
        if not user_exists(telegram_id):
            create_user(telegram_id)

        # Continue processing with other handlers
        return HandlerStatus.CONTINUE
