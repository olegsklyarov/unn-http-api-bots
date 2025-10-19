import bot.database_client

from bot.handler import Handler
from bot.handler_result import HandlerStatus


class UpdateDatabaseLogger(Handler):
    """
    Должен быть добавлен первым обработчиком
    """

    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        return True

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        bot.database_client.persist_update(update)
        return HandlerStatus.CONTINUE
