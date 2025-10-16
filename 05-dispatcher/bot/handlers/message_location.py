import bot.telegram_api_client
from bot.filters import is_message_with_location
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageLocation(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_location(update)

    def handle(self, update: dict) -> HandlerStatus:
        location = update['message']['location']
        bot.telegram_api_client.send_message(
            chat_id=update['message']['chat']['id'],
            text=f"Received location: lat={location.get('latitude')} lon={location.get('longitude')}",
        )
        return HandlerStatus.STOP


