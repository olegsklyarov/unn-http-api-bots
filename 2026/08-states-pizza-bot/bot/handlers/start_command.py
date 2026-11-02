from bot import pizza_menu
from bot import telegram_bot_api
from bot import users_storage
from bot.handler import Handler
from bot.handler import HandlerStatus


class StartCommand(Handler):
    def can_handle(self, update: dict, state: dict) -> bool:
        if "message" not in update:
            return False
        text = update["message"].get("text")
        if text is None:
            return False
        return text.split("@", 1)[0] == "/start"

    def handle(self, update: dict, state: dict) -> HandlerStatus:
        message = update["message"]
        user_id = message["from"]["id"]
        new_state = users_storage.default_state()
        users_storage.save_user_state(user_id, new_state)
        telegram_bot_api.send_message(
            chat_id=message["chat"]["id"],
            text=pizza_menu.MSG_CHOOSE_RECIPE,
            reply_markup=pizza_menu.recipes_keyboard(),
        )
        return HandlerStatus.STOP
