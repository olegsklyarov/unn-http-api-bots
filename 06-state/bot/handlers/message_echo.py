import bot.telegram_api_client
from bot.filters import is_message_with_text
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageEcho(Handler):
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        return is_message_with_text(update)

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text=update["message"]["text"],
        )
        return HandlerStatus.STOP
