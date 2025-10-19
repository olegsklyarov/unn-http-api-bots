import json

import bot.telegram_api_client
from bot.database_client import clear_user_data, update_user_state
from bot.filters import is_message_with_text
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class MessageStart(Handler):
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        return is_message_with_text(update) and update['message']['text'] == '/start'

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        telegram_id = update["message"]["from"]["id"]

        # Clear any existing user state and data
        clear_user_data(telegram_id)

        # Update user state to wait for pizza selection
        update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        # Clear any existing keyboard first
        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text="🍕 Welcome to Pizza shop!",
            reply_markup=json.dumps({"remove_keyboard": True}),
        )

        # Send pizza selection message with inline keyboard
        bot.telegram_api_client.send_message(
            chat_id=update["message"]["chat"]["id"],
            text="Please choose pizza type",
            reply_markup=json.dumps(
                {
                    'inline_keyboard': [
                        [
                            {"text": "Margherita", "callback_data": "pizza_margherita"},
                            {"text": "Pepperoni", "callback_data": "pizza_pepperoni"},
                        ],
                        [
                            {"text": "Quattro Stagioni", "callback_data": "pizza_quattro_stagioni"},
                            {"text": "Capricciosa", "callback_data": "pizza_capricciosa"},
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
