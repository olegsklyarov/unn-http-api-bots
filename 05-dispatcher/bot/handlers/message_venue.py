import bot.telegram_api_client
from bot.filters import is_message_with_venue
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageVenue(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_venue(update)

    def handle(self, update: dict) -> HandlerStatus:
        venue = update['message']['venue']
        title = venue.get('title', '')
        address = venue.get('address', '')
        bot.telegram_api_client.send_message(
            chat_id=update['message']['chat']['id'],
            text=f"Received venue: {title} — {address}",
        )
        return HandlerStatus.STOP


