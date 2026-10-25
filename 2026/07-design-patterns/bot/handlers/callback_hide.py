import json

from bot import telegram_bot_api
from bot.handler import Handler
from bot.handler import HandlerStatus


class CallbackHide(Handler):
    def can_handle(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"].get("data") == "hide"
        )

    def handle(self, update: dict) -> HandlerStatus:
        cq = update["callback_query"]
        # Без answerCallbackQuery у кнопки бесконечно крутятся «часики».
        telegram_bot_api.answer_callback_query(callback_query_id=cq["id"])
        message = cq.get("message")
        if message is None:
            return HandlerStatus.STOP
        telegram_bot_api.edit_message_reply_markup(
            chat_id=message["chat"]["id"],
            message_id=message["message_id"],
            reply_markup=json.dumps({"inline_keyboard": []}),
        )
        return HandlerStatus.STOP
