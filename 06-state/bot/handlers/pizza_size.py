import json

import bot.telegram_api_client
import bot.database_client
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class PizzaSizeHandler(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_PIZZA_SIZE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("size_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        size_mapping = {
            "size_small": "Small (25cm)",
            "size_medium": "Medium (30cm)",
            "size_large": "Large (35cm)",
            "size_xl": "Extra Large (40cm)",
        }

        pizza_size = size_mapping.get(callback_data)
        data["pizza_size"] = pizza_size
        bot.database_client.update_user_data(telegram_id, data)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_DRINKS")

        bot.telegram_api_client.answer_callback_query(update["callback_query"]["id"])

        bot.telegram_api_client.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        bot.telegram_api_client.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Please choose some drinks",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "Coca-Cola", "callback_data": "drink_coca_cola"},
                            {"text": "Pepsi", "callback_data": "drink_pepsi"},
                        ],
                        [
                            {
                                "text": "Orange Juice",
                                "callback_data": "drink_orange_juice",
                            },
                            {
                                "text": "Apple Juice",
                                "callback_data": "drink_apple_juice",
                            },
                        ],
                        [
                            {"text": "Water", "callback_data": "drink_water"},
                            {"text": "Iced Tea", "callback_data": "drink_iced_tea"},
                        ],
                        [
                            {"text": "No drinks", "callback_data": "drink_none"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
