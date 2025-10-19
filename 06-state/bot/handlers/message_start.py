import json

import bot.telegram_api_client
import bot.database_client
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class MessageStart(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        return (
            "message" in update
            and "text" in update["message"]
            and update["message"]["text"] == "/start"
        )

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        bot.database_client.clear_user_data(telegram_id)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text="🍕 Welcome to Pizza shop!",
            reply_markup=json.dumps({"remove_keyboard": True}),
        )

        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text="Please choose pizza type",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Margherita", "callback_data": "pizza_margherita"},
                            {"text": "Pepperoni", "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {
                                "text": "Quattro Stagioni",
                                "callback_data": "pizza_quattro_stagioni",
                            },
                            {
                                "text": "Capricciosa",
                                "callback_data": "pizza_capricciosa",
                            },
                        ],
                        [
                            {"text": "Diavola", "callback_data": "pizza_diavola"},
                            {"text": "Prosciutto", "callback_data": "pizza_prosciutto"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
