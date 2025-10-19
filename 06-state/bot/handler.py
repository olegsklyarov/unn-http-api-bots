from abc import ABC, abstractmethod

from bot.handler_result import HandlerStatus


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        pass

    @abstractmethod
    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        pass
