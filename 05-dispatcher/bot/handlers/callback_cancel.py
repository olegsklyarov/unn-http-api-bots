import bot.telegram_api_client
from bot.constants import CALLBACK_CANCEL
from bot.filters import is_callback_query
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class CallbackCancel(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_callback_query(update) and update['callback_query']['data'] == CALLBACK_CANCEL

    def handle(self, update: dict) -> HandlerStatus:
        bot.telegram_api_client.answer_callback_query(update['callback_query']['id'])
        bot.telegram_api_client.delete_message(
            update['callback_query']['message']['chat']['id'],
            update['callback_query']['message']['message_id'],
        )
        return HandlerStatus.STOP
