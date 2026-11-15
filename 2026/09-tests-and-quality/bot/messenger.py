from abc import ABC, abstractmethod
from typing import Optional


class Messenger(ABC):
    @abstractmethod
    def user_id_from_update(self, update: dict) -> Optional[int]:
        pass

    @abstractmethod
    def get_updates(self, **params):
        pass

    @abstractmethod
    def send_message(self, **params):
        pass

    @abstractmethod
    def answer_callback_query(self, **params):
        pass
