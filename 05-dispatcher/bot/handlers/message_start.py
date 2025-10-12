import json

import bot.telegram_api_client
from bot.constants import BUTTON_INLINE
from bot.filters import is_message_with_text
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageStart(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_text(update) and update['message']['text'] == '/start'

    def handle(self, update: dict) -> HandlerStatus:
        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text="Welcome 👋",
            reply_markup=json.dumps(
                {
                    'keyboard': [
                        [
                            {"text": BUTTON_INLINE},
                            {"text": "Top-Right"},
                        ],
                        [
                            {"text": "Top-Left"},
                            {"text": "Bottom-Left"},
                        ],
                    ],
                    'resize_keyboard': True
                },
            ),
        )
        return HandlerStatus.STOP
