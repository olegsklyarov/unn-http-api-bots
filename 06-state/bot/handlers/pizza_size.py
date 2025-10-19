import json

import bot.telegram_api_client
from bot.database_client import get_user, update_user_data, update_user_state
from bot.filters import is_callback_query
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class PizzaSizeHandler(Handler):
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        # Check if it's a callback query and user is waiting for pizza size
        if not is_callback_query(update):
            return False

        # Check if user state is WAIT_FOR_PIZZA_SIZE
        if not user_state or user_state.get('state') != 'WAIT_FOR_PIZZA_SIZE':
            return False

        # Check if callback data starts with 'size_'
        callback_data = update['callback_query']['data']
        return callback_data.startswith('size_')

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        # Extract pizza size from callback data (remove 'size_' prefix)
        size_mapping = {
            'size_small': 'Small (25cm)',
            'size_medium': 'Medium (30cm)',
            'size_large': 'Large (35cm)',
            'size_xl': 'Extra Large (40cm)'
        }
        pizza_size = size_mapping.get(callback_data, callback_data.replace('size_', '').title())

        # Get current user data to preserve pizza name
        current_user = get_user(telegram_id)
        current_data = current_user.get('data', '') if current_user else ''

        # Parse existing data if it's JSON, otherwise create new object
        try:
            if current_data:
                order_data = json.loads(current_data)
            else:
                order_data = {}
        except (json.JSONDecodeError, TypeError):
            # If data is not valid JSON, treat it as pizza name for backward compatibility
            order_data = {'pizza_name': current_data} if current_data else {}

        # Add pizza size to order data
        order_data['pizza_size'] = pizza_size

        # Save order data as JSON
        update_user_data(telegram_id, order_data)

        # Update user state to wait for drinks
        update_user_state(telegram_id, "WAIT_FOR_DRINKS")

        # Answer the callback query
        bot.telegram_api_client.answer_callback_query(update['callback_query']['id'])

        # Delete the previous message with pizza size selection
        bot.telegram_api_client.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"]
        )

        # Send drinks selection message
        bot.telegram_api_client.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text="Please choose some drinks",
            reply_markup=json.dumps(
                {
                    'inline_keyboard': [
                        [
                            {"text": "Coca-Cola", "callback_data": "drink_coca_cola"},
                            {"text": "Pepsi", "callback_data": "drink_pepsi"},
                        ],
                        [
                            {"text": "Orange Juice", "callback_data": "drink_orange_juice"},
                            {"text": "Apple Juice", "callback_data": "drink_apple_juice"},
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
