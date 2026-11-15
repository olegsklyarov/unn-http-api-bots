from bot import telegram_bot_api
from bot.messenger import Messenger

# Update payloads that wrap a Message (optional .from)
_MESSAGE_KEYS = (
    "message",
    "edited_message",
    "channel_post",
    "edited_channel_post",
    "business_message",
    "edited_business_message",
)

# Update payloads with required/optional User in .from
_FROM_KEYS = (
    "callback_query",
    "inline_query",
    "chosen_inline_result",
    "shipping_query",
    "pre_checkout_query",
    "my_chat_member",
    "chat_member",
    "chat_join_request",
    "purchased_paid_media",
    "message_reaction",
)

# Update payloads with User in .user
_USER_KEYS = (
    "poll_answer",
    "business_connection",
)


class TelegramMessenger(Messenger):
    def get_updates(self, **params):
        return telegram_bot_api.get_updates(**params)

    def send_message(self, **params):
        return telegram_bot_api.send_message(**params)

    def send_sticker(self, **params):
        return telegram_bot_api.send_sticker(**params)

    def send_video_note(self, **params):
        return telegram_bot_api.send_video_note(**params)

    def answer_callback_query(self, **params):
        return telegram_bot_api.answer_callback_query(**params)

    def edit_message_reply_markup(self, **params):
        return telegram_bot_api.edit_message_reply_markup(**params)

    def user_from_update(self, update):
        for key in _MESSAGE_KEYS:
            if key in update:
                return update[key].get("from")
        for key in _FROM_KEYS:
            if key in update:
                return update[key].get("from")
        for key in _USER_KEYS:
            if key in update:
                return update[key].get("user")
        return None

    def user_id_from_update(self, update: dict) -> int | None:
        user = self.user_from_update(update)
        if user is None:
            return None
        return int(user["id"])
