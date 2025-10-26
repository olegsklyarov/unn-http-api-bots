from abc import ABC, abstractmethod

from bot.handler_result import HandlerStatus


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        pass

    @abstractmethod
    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        pass
