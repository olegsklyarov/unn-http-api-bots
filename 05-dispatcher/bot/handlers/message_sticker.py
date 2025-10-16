import bot.telegram_api_client
from bot.filters import is_message_with_sticker
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageSticker(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_sticker(update)

    def handle(self, update: dict) -> HandlerStatus:
        sticker = update['message']['sticker']
        if 'file_id' in sticker:
            response = bot.telegram_api_client.get_file(sticker['file_id'])
            bot.telegram_api_client.download_file(response['file_path'])
        return HandlerStatus.STOP


