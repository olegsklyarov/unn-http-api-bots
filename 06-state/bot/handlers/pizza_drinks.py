import json

import bot.telegram_api_client
from bot.database_client import get_user, update_user_data, update_user_state
from bot.filters import is_callback_query
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class PizzaDrinksHandler(Handler):
    def can_handle(self, update: dict, user_state: dict = None) -> bool:
        # Check if it's a callback query and user is waiting for drinks
        if not is_callback_query(update):
            return False

        # Check if user state is WAIT_FOR_DRINKS
        if not user_state or user_state.get('state') != 'WAIT_FOR_DRINKS':
            return False

        # Check if callback data starts with 'drink_'
        callback_data = update['callback_query']['data']
        return callback_data.startswith('drink_')

    def handle(self, update: dict, user_state: dict = None) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        # Extract drink name from callback data (remove 'drink_' prefix)
        drink_mapping = {
            'drink_coca_cola': 'Coca-Cola',
            'drink_pepsi': 'Pepsi',
            'drink_orange_juice': 'Orange Juice',
            'drink_apple_juice': 'Apple Juice',
            'drink_water': 'Water',
            'drink_iced_tea': 'Iced Tea',
            'drink_none': 'No drinks'
        }
        selected_drink = drink_mapping.get(callback_data, callback_data.replace('drink_', '').replace('_', ' ').title())

        # Get current user data to preserve existing order
        current_user = get_user(telegram_id)
        current_data = current_user.get('data', '') if current_user else ''

        # Parse existing data if it's JSON, otherwise create new object
        try:
            if current_data:
                order_data = json.loads(current_data)
            else:
                order_data = {}
        except (json.JSONDecodeError, TypeError):
            # If data is not valid JSON, create new object
            order_data = {}

        # Add selected drink to order data
        order_data['drink'] = selected_drink

        # Save updated order data as JSON
        update_user_data(telegram_id, order_data)

        # Update user state to wait for order approval
        update_user_state(telegram_id, "WAIT_FOR_ORDER_APPROVE")

        # Answer the callback query
        bot.telegram_api_client.answer_callback_query(update['callback_query']['id'])

        # Delete the previous message with drinks selection
        bot.telegram_api_client.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"]
        )

        # Create order summary message
        pizza_name = order_data.get('pizza_name', 'Unknown')
        pizza_size = order_data.get('pizza_size', 'Unknown')
        drink = order_data.get('drink', 'Unknown')

        order_summary = f"""🍕 **Your Order Summary:**

**Pizza:** {pizza_name}
**Size:** {pizza_size}
**Drink:** {drink}

Is everything correct?"""

        # Send order approval message
        bot.telegram_api_client.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            text=order_summary,
            parse_mode="Markdown",
            reply_markup=json.dumps(
                {
                    'inline_keyboard': [
                        [
                            {"text": "✅ Ok", "callback_data": "order_approve"},
                            {"text": "🔄 Start again", "callback_data": "order_restart"},
                        ],
                    ],
                },
            ),
        )
        return HandlerStatus.STOP
