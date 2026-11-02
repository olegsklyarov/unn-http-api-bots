import json

from bot import telegram_bot_api
from bot.handler import Handler
from bot.handler import HandlerStatus


class CallbackRawJson(Handler):
    def can_handle(self, update: dict) -> bool:
        return (
            "callback_query" in update
            and update["callback_query"].get("data") == "raw"
        )

    def handle(self, update: dict) -> HandlerStatus:
        cq = update["callback_query"]
        # Без answerCallbackQuery у кнопки бесконечно крутятся «часики».
        telegram_bot_api.answer_callback_query(callback_query_id=cq["id"])
        message = cq.get("message")
        if message is None:
            return HandlerStatus.STOP
        reply_to_message = message.get("reply_to_message")
        if reply_to_message is None:
            return HandlerStatus.STOP
        raw = json.dumps(reply_to_message, ensure_ascii=False, indent=2)
        telegram_bot_api.send_message(
            chat_id=message["chat"]["id"],
            text=f"```\n{raw}\n```",
            parse_mode="Markdown",
        )
        return HandlerStatus.STOP
