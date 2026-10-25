from abc import ABC, abstractmethod
from enum import Enum


class HandlerStatus(Enum):
    CONTINUE = 1
    STOP = 2


class Handler(ABC):
    @abstractmethod
    def can_handle(self, update: dict) -> bool:
        pass

    @abstractmethod
    def handle(self, update: dict) -> HandlerStatus:
        pass
