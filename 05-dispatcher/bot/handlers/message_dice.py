import bot.telegram_api_client
from bot.filters import is_message_with_dice
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageDice(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_dice(update)

    def handle(self, update: dict) -> HandlerStatus:
        dice = update['message']['dice']
        value = dice.get('value')
        emoji = dice.get('emoji', '🎲')
        bot.telegram_api_client.send_message(
            chat_id=update['message']['chat']['id'],
            text=f"Received dice {emoji}: {value}",
        )
        return HandlerStatus.STOP


