import bot.database_client

from bot.handler import Handler
from bot.handler_result import HandlerStatus


class UpdateDatabaseLogger(Handler):
    def can_handle(self, update: dict) -> bool:
        return True

    def handle(self, update: dict) -> HandlerStatus:
        bot.database_client.persist_update(update)
        return HandlerStatus.CONTINUE
