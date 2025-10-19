import json

import bot.telegram_api_client
import bot.database_client
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class PizzaDrinksHandler(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_DRINKS":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data.startswith("drink_")

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        # Extract drink name from callback data (remove 'drink_' prefix)
        drink_mapping = {
            "drink_coca_cola": "Coca-Cola",
            "drink_pepsi": "Pepsi",
            "drink_orange_juice": "Orange Juice",
            "drink_apple_juice": "Apple Juice",
            "drink_water": "Water",
            "drink_iced_tea": "Iced Tea",
            "drink_none": "No drinks",
        }
        selected_drink = drink_mapping.get(callback_data)

        data["drink"] = selected_drink

        bot.database_client.update_user_data(telegram_id, data)
        bot.database_client.update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")
        bot.telegram_api_client.answer_callback_query(update["callback_query"]["id"])

        bot.telegram_api_client.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        # Create order summary message
        pizza_name = data.get("pizza_name", "Unknown")
        pizza_size = data.get("pizza_size", "Unknown")
        drink = data.get("drink", "Unknown")

        order_summary = f"""🍕 **Your Order Summary:**

**Pizza:** {pizza_name}
**Size:** {pizza_size}
**Drink:** {drink}

Is everything correct?"""

        bot.telegram_api_client.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
            parse_mode="Markdown",
            reply_markup=json.dumps(
                {
                    "inline_keyboard": [
                        [
                            {"text": "✅ Ok", "callback_data": "order_approve"},
                            {
                                "text": "🔄 Start again",
                                "callback_data": "order_restart",
                            },
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
