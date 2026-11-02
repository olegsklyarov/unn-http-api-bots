from bot import pizza_menu
from bot import telegram_bot_api
from bot import users_storage
from bot.handler import Handler
from bot.handler import HandlerStatus

_VALID = {key for key, _ in pizza_menu.DRINKS}


class WaitingForDrink(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        if state.get("current_state") != "waiting_for_drink":
            return False
        if "callback_query" not in update:
            return False
        data = update["callback_query"].get("data", "")
        value = pizza_menu.parse_callback_data(data, "drink")
        return value is not None and value in _VALID

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        cq = update["callback_query"]
        telegram_bot_api.answer_callback_query(callback_query_id=cq["id"])
        drink = pizza_menu.parse_callback_data(cq["data"], "drink")
        state["order_content"]["drink"] = drink
        state["current_state"] = "order_finished"
        users_storage.save_user_state(cq["from"]["id"], state)
        telegram_bot_api.send_message(
            chat_id=cq["message"]["chat"]["id"],
            text=pizza_menu.format_order_summary(state["order_content"]),
        )
        return HandlerStatus.STOP
