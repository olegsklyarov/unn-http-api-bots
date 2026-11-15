from bot.handler import Handler
from bot.handler import HandlerStatus
from bot.messenger import Messenger
from bot.storage import Storage


class PersistUpdate(Handler):
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
        storage.persist_update(update)
        return HandlerStatus.CONTINUE
