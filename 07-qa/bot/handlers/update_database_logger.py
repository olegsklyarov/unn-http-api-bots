import bot.database_client
from bot.handler_result import HandlerStatus
from bot.handlers.handler import Handler


class UpdateDatabaseLogger(Handler):
    """
    Должен быть добавлен первым обработчиком
    """

    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        return True

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        bot.database_client.persist_update(update)
        return HandlerStatus.CONTINUE
