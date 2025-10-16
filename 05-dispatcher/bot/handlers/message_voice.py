import bot.telegram_api_client
from bot.filters import is_message_with_voice
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageVoice(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_voice(update)

    def handle(self, update: dict) -> HandlerStatus:
        response = bot.telegram_api_client.get_file(update['message']['voice']['file_id'])
        bot.telegram_api_client.download_file(response['file_path'])
        return HandlerStatus.STOP


