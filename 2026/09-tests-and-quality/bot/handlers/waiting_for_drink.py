from bot import pizza_menu
from bot.handler import Handler
from bot.handler import HandlerStatus
from bot.messenger import Messenger
from bot.storage import Storage

_VALID = {key for key, _ in pizza_menu.DRINKS}


class WaitingForDrink(Handler):
    def can_handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if state.get("current_state") != "waiting_for_drink":
            return False
        if "callback_query" not in update:
            return False
        data = update["callback_query"].get("data", "")
        value = pizza_menu.parse_callback_data(data, "drink")
        return value is not None and value in _VALID

    def handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        cq = update["callback_query"]
        messenger.answer_callback_query(callback_query_id=cq["id"])
        drink = pizza_menu.parse_callback_data(cq["data"], "drink")
        state["order_content"]["drink"] = drink
        state["current_state"] = "order_finished"
        storage.save_user_state(cq["from"]["id"], state)
        messenger.send_message(
            chat_id=cq["message"]["chat"]["id"],
            text=pizza_menu.format_order_summary(state["order_content"]),
        )
        return HandlerStatus.STOP
