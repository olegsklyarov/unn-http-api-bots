from bot import pizza_menu
from bot.handler import Handler
from bot.handler import HandlerStatus
from bot.messenger import Messenger
from bot.storage import Storage


class OrderFinished(Handler):
    def can_handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> bool:
        return (
            state.get("current_state") == "order_finished"
            and "callback_query" in update
        )

    def handle(
        self,
        update: dict,
        state: dict,
        storage: Storage,
        messenger: Messenger,
    ) -> HandlerStatus:
        cq = update["callback_query"]
        messenger.answer_callback_query(callback_query_id=cq["id"])
        message = cq.get("message")
        if message is not None:
            messenger.send_message(
                chat_id=message["chat"]["id"],
                text=pizza_menu.MSG_ORDER_FINISHED_HINT,
            )
        return HandlerStatus.STOP
