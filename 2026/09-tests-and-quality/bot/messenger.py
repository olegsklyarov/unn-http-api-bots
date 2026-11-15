from abc import ABC, abstractmethod


class Messenger(ABC):
    @abstractmethod
    def user_id_from_update(self, update: dict) -> int | None:
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

    @abstractmethod
    def delete_message(self, **params):
        pass
