"""Первый handler в цепочке: сохранить Update на диск.

can_handle всегда True; CONTINUE — чтобы дальше шли users и echo/callback.
"""

from bot import updated_logger
from bot.handler import Handler
from bot.handler import HandlerStatus


class PersistUpdate(Handler):
    def can_handle(self, update: dict) -> bool:
        return True

    def handle(self, update: dict) -> HandlerStatus:
        updated_logger.persist_update(update)
        return HandlerStatus.CONTINUE
