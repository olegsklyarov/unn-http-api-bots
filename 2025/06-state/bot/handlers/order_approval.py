import json

import bot.telegram_api_client
from bot.database_client import clear_user_data, update_user_state
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class OrderApprovalHandler(Handler):
    def can_handle(self, update: dict, state: str, data: dict) -> bool:
        if "callback_query" not in update:
            return False

        if state != "WAIT_FOR_ORDER_APPROVE":
            return False

        callback_data = update["callback_query"]["data"]
        return callback_data in ["order_approve", "order_restart"]

    def handle(self, update: dict, state: str, data: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        bot.telegram_api_client.answer_callback_query(update["callback_query"]["id"])
        bot.telegram_api_client.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"],
        )

        if callback_data == "order_approve":
            update_user_state(telegram_id, "ORDER_FINISHED")

            pizza_name = data.get("pizza_name", "Unknown")
            pizza_size = data.get("pizza_size", "Unknown")
            drink = data.get("drink", "Unknown")

            order_confirmation = f"""✅ **Order Confirmed!**
🍕 **Your Order:**
• Pizza: {pizza_name}
• Size: {pizza_size}
• Drink: {drink}

Thank you for your order! Your pizza will be ready soon.

Send /start to place another order."""

            # Send order confirmation message
            bot.telegram_api_client.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text=order_confirmation,
                parse_mode="Markdown",
            )

        elif callback_data == "order_restart":
            clear_user_data(telegram_id)

            # Update user state to wait for pizza selection
            update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

            # Send pizza selection message with inline keyboard
            bot.telegram_api_client.send_message(
                chat_id=update["callback_query"]["message"]["chat"]["id"],
                text="Please choose pizza type",
                reply_markup=json.dumps(
                    {
                        "inline_keyboard": [
                            [
                                {
                                    "text": "Margherita",
                                    "callback_data": "pizza_margherita",
                                },
                                {
                                    "text": "Pepperoni",
                                    "callback_data": "pizza_pepperoni",
                                },
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
                                {
                                    "text": "Prosciutto",
                                    "callback_data": "pizza_prosciutto",
                                },
                            ],
                        ],
                    },
                ),
            )

        return HandlerStatus.STOP
