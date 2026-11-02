from bot import users_storage
from bot.handler import Handler
from bot.handler import HandlerStatus


class PersistUser(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        return True

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        users_storage.persist_user(update)
        return HandlerStatus.CONTINUE
