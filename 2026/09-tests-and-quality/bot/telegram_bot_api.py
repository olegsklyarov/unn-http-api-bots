import json
import os
import urllib.parse
import urllib.request
from typing import Optional

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
    def __init__(self) -> None:
        self._token = os.environ["TELEGRAM_TOKEN"]
        self._base_url = os.environ["TELEGRAM_BASE_URL"]

    def api_request(self, method, **params):
        url = f"{self._base_url}{self._token}/{method}"
        # url = f"https://api.telegram.org/bot{self._token}/{method}"
        data = urllib.parse.urlencode(params).encode()
        with urllib.request.urlopen(url, data=data) as r:
            payload = json.loads(r.read())
        assert payload["ok"]
        return payload

    def get_updates(self, **params):
        return self.api_request("getUpdates", **params)["result"]

    def send_message(self, **params):
        return self.api_request("sendMessage", **params)

    def send_sticker(self, **params):
        return self.api_request("sendSticker", **params)

    def send_video_note(self, **params):
        return self.api_request("sendVideoNote", **params)

    def answer_callback_query(self, **params):
        return self.api_request("answerCallbackQuery", **params)

    def edit_message_reply_markup(self, **params):
        return self.api_request("editMessageReplyMarkup", **params)

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

    def user_id_from_update(self, update: dict) -> Optional[int]:
        user = self.user_from_update(update)
        if user is None:
            return None
        return int(user["id"])
