"""Echo стикера по file_id + те же inline-кнопки.

sendSticker: https://core.telegram.org/bots/api#sendsticker
"""

import json

from bot import telegram_bot_api
from bot.handler import Handler
from bot.handler import HandlerStatus


class MessageEchoSticker(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "sticker" in update["message"]

    def handle(self, update: dict) -> HandlerStatus:
        message = update["message"]
        telegram_bot_api.send_sticker(
            chat_id=message["chat"]["id"],
            sticker=message["sticker"]["file_id"],
            reply_to_message_id=message["message_id"],
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Сырой JSON", "callback_data": "raw"},
                            {"text": "Скрыть", "callback_data": "hide"},
                        ]
                    ]
                },
                ensure_ascii=False,
            ),
        )
        return HandlerStatus.STOP
