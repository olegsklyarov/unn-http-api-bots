import json

import bot.telegram_api_client
from bot.database_client import clear_user_data, get_user, update_user_state
from bot.filters import is_callback_query
from bot.handlers.handler import Handler
from bot.handler_result import HandlerStatus


class OrderApprovalHandler(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        # Check if it's a callback query and user is waiting for order approval
        if not is_callback_query(update):
            return False

        # Check if user state is WAIT_FOR_ORDER_APPROVE
        if not user_state or user_state.get('state') != 'WAIT_FOR_ORDER_APPROVE':
            return False

        # Check if callback data is order_approve or order_restart
        callback_data = update['callback_query']['data']
        return callback_data in ['order_approve', 'order_restart']

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        telegram_id = update["callback_query"]["from"]["id"]
        callback_data = update["callback_query"]["data"]

        # Answer the callback query
        bot.telegram_api_client.answer_callback_query(update['callback_query']['id'])

        # Delete the previous message with order summary
        bot.telegram_api_client.delete_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
            message_id=update["callback_query"]["message"]["message_id"]
        )

        if callback_data == 'order_approve':
            # Handle order approval
            self._handle_order_approval(update, telegram_id)
        elif callback_data == 'order_restart':
            # Handle order restart
            self._handle_order_restart(update, telegram_id)

        return HandlerStatus.STOP

    def _handle_order_approval(self, update: dict, telegram_id: int) -> None:
        """Handle order approval - show final order details."""
        # Update user state to finished
        update_user_state(telegram_id, "ORDER_FINISHED")

        # Get order details
        current_user = get_user(telegram_id)
        current_data = current_user.get('data', '') if current_user else ''

        try:
            if current_data:
                order_data = json.loads(current_data)
            else:
                order_data = {}
        except (json.JSONDecodeError, TypeError):
            order_data = {}

        # Create order confirmation message
        pizza_name = order_data.get('pizza_name', 'Unknown')
        pizza_size = order_data.get('pizza_size', 'Unknown')
        drink = order_data.get('drink', 'Unknown')

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
            parse_mode="Markdown"
        )

    def _handle_order_restart(self, update: dict, telegram_id: int) -> None:
        """Handle order restart - clear data and start from beginning."""
        # Clear any existing user state and data
        clear_user_data(telegram_id)

        # Update user state to wait for pizza selection
        update_user_state(telegram_id, "WAIT_FOR_PIZZA_NAME")

        # Send pizza selection message with inline keyboard
        bot.telegram_api_client.send_message(
            chat_id=update["callback_query"]["message"]["chat"]["id"],
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
