from bot import pizza_menu
from bot.handler import Handler, HandlerStatus
from bot.messenger import Messenger
from bot.storage import Storage

_VALID = {key for key, _ in pizza_menu.RECIPES}


class WaitingForRecipe(Handler):
    def can_handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        if state.get("current_state") != "waiting_for_recipe":
            return False
        if "callback_query" not in update:
            return False
        data = update["callback_query"].get("data", "")
        value = pizza_menu.parse_callback_data(data, "recipe")
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
        message = cq["message"]
        messenger.delete_message(
            chat_id=message["chat"]["id"],
            message_id=message["message_id"],
        )
        recipe = pizza_menu.parse_callback_data(cq["data"], "recipe")
        state["order_content"]["recipe"] = recipe
        state["current_state"] = "waiting_for_pizza_size"
        storage.save_user_state(cq["from"]["id"], state)
        messenger.send_message(
            chat_id=message["chat"]["id"],
            text=pizza_menu.step_message(
                state["order_content"], pizza_menu.MSG_CHOOSE_SIZE
            ),
            reply_markup=pizza_menu.sizes_keyboard(),
        )
        return HandlerStatus.STOP
