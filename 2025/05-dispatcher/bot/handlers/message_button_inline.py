import json

import bot.telegram_api_client
from bot.constants import BUTTON_INLINE, CALLBACK_CANCEL
from bot.filters import is_message_with_text
from bot.handler import Handler
from bot.handler_result import HandlerStatus


class MessageButtonInline(Handler):
    def can_handle(self, update: dict) -> bool:
        return is_message_with_text(update) and update['message']['text'] == BUTTON_INLINE

    def handle(self, update: dict) -> HandlerStatus:
        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text="This is inline keyboard",
            reply_markup=json.dumps(
                {
                    'inline_keyboard': [
                        [
                            {"text": "Открыть wiki", "url": "https://wiki.olegsklyarov.ru"},
                            {"text": "Отмена", "callback_data": CALLBACK_CANCEL},
                        ],
                    ],
                    'resize_keyboard': True
                },
            ),
        )
        return HandlerStatus.STOP
