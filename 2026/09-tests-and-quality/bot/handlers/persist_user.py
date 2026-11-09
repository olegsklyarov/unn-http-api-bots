from bot.handler import Handler
from bot.handler import HandlerStatus
from bot.messenger import Messenger
from bot.storage import Storage


class PersistUser(Handler):
    def can_handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return True

    def handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        storage.persist_user(update)
        return HandlerStatus.CONTINUE
