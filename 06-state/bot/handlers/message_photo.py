import bot.telegram_api_client
from bot.filters import is_message_with_photo
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class MessagePhoto(Handler):
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        return is_message_with_photo(update)

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        response = bot.telegram_api_client.get_file(update['message']['photo'][-1]['file_id'])
        bot.telegram_api_client.download_file(response['file_path'])
        return HandlerStatus.STOP
