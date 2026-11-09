from abc import ABC, abstractmethod


class Storage(ABC):
    @abstractmethod
    def get_user_state(self, user_id) -> dict:
        pass

    @abstractmethod
    def save_user_state(self, user_id, state: dict) -> None:
        pass

    @abstractmethod
    def persist_user(self, update: dict) -> None:
        pass

    @abstractmethod
    def default_state(self) -> dict:
        pass
