import bot.telegram_api_client
from bot.filters import is_message_with_contact
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageContact(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_contact(update)

    def handle(self, update: dict) -> HandlerStatus:
        contact = update['message']['contact']
        bot.telegram_api_client.send_message(
            chat_id=update['message']['chat']['id'],
            text=f"Received contact: {contact.get('first_name', '')} {contact.get('last_name', '')} {contact.get('phone_number', '')}".strip(),
        )
        return HandlerStatus.STOP


