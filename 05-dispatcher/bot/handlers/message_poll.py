import bot.telegram_api_client
from bot.filters import is_message_with_type
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessagePoll(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_type(update, 'poll')

    def handle(self, update: dict) -> HandlerStatus:
        poll = update['message']['poll']
        question = poll.get('question', 'poll')
        bot.telegram_api_client.send_message(
            chat_id=update['message']['chat']['id'],
            text=f"Received poll: {question}",
        )
        return HandlerStatus.STOP


