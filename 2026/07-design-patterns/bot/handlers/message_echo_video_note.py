"""Echo video note (кружок) по file_id + inline-кнопки.

sendVideoNote: https://core.telegram.org/bots/api#sendvideonote
"""

import json

from bot import telegram_bot_api
from bot.handler import Handler
from bot.handler import HandlerStatus


class MessageEchoVideoNote(Handler):
    def can_handle(self, update: dict) -> bool:
        return "message" in update and "video_note" in update["message"]

    def handle(self, update: dict) -> HandlerStatus:
        message = update["message"]
        telegram_bot_api.send_video_note(
            chat_id=message["chat"]["id"],
            video_note=message["video_note"]["file_id"],
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
