from bot import pizza_menu
from bot import telegram_bot_api
from bot import users_storage
from bot.handler import Handler
from bot.handler import HandlerStatus

_VALID = {key for key, _ in pizza_menu.SIZES}


class WaitingForPizzaSize(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        if state.get("current_state") != "waiting_for_pizza_size":
            return False
        if "callback_query" not in update:
            return False
        data = update["callback_query"].get("data", "")
        value = pizza_menu.parse_callback_data(data, "size")
        return value is not None and value in _VALID

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        cq = update["callback_query"]
        telegram_bot_api.answer_callback_query(callback_query_id=cq["id"])
        size = pizza_menu.parse_callback_data(cq["data"], "size")
        state["order_content"]["size"] = size
        state["current_state"] = "waiting_for_crust"
        users_storage.save_user_state(cq["from"]["id"], state)
        telegram_bot_api.send_message(
            chat_id=cq["message"]["chat"]["id"],
            text=pizza_menu.MSG_CHOOSE_CRUST,
            reply_markup=pizza_menu.crusts_keyboard(),
        )
        return HandlerStatus.STOP
