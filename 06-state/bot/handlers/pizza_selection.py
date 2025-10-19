import json

import bot.telegram_api_client
from bot.database_client import update_user_data, update_user_state
from bot.filters import is_callback_query
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class PizzaSelectionHandler(Handler):
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        # Check if it's a callback query and user is waiting for pizza selection
        if not is_callback_query(update):
            return False

        # Check if user state is WAIT_FOR_PIZZA_NAME
        if not user_state or user_state.get('state') != 'WAIT_FOR_PIZZA_NAME':
            return False

        # Check if callback data starts with 'pizza_'
        callback_data = update['callback_query']['data']
        return callback_data.startswith('pizza_')

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        # Extract pizza name from callback data (remove 'pizza_' prefix)
        pizza_name = callback_data.replace('pizza_', '').replace('_', ' ').title()

        # Save pizza name in user data
        update_user_data(telegram_id, {"pizza_name": pizza_name})

        # Update user state to wait for pizza size
        update_user_state(telegram_id, "WAIT_FOR_PIZZA_SIZE")

        # Answer the callback query
        bot.telegram_api_client.answer_callback_query(update['callback_query']['id'])

        # Send pizza size selection message
        bot.telegram_api_client.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Please select pizza size",
            reply_markup=json.dumps(
                {
                    'inline_keyboard': [
                        [
                            {"text": "Small (25cm)", "callback_data": "size_small"},
                            {"text": "Medium (30cm)", "callback_data": "size_medium"},
                        ],
                        [
                            {"text": "Large (35cm)", "callback_data": "size_large"},
                            {"text": "Extra Large (40cm)", "callback_data": "size_xl"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
