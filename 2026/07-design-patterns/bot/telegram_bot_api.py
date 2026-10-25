"""Тонкий HTTP-клиент Telegram Bot API.

Вынесен в модуль, чтобы отделить транспорт от логики бота.
https://docs.python.org/3/tutorial/modules.html
https://docs.python.org/3/library/urllib.request.html
https://core.telegram.org/bots/api
"""

import json
import os
import urllib.parse
import urllib.request

TOKEN = os.environ["TELEGRAM_TOKEN"]


def api_request(method, **params):
    url = f"https://api.telegram.org/bot{TOKEN}/{method}"
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(url, data=data) as r:
        payload = json.loads(r.read())
    assert payload["ok"]
    return payload


def get_updates(**params):
    return api_request("getUpdates", **params)["result"]


def send_message(**params):
    return api_request("sendMessage", **params)


def send_sticker(**params):
    return api_request("sendSticker", **params)


def send_video_note(**params):
    return api_request("sendVideoNote", **params)


def answer_callback_query(**params):
    return api_request("answerCallbackQuery", **params)


def edit_message_reply_markup(**params):
    return api_request("editMessageReplyMarkup", **params)
