import json
import os
import urllib.parse
import urllib.request

BASE_URL = os.environ["BASE_URL"]
TOKEN = os.environ["TELEGRAM_TOKEN"]


def api(method, **params):
    url = f"{BASE_URL}/bot{TOKEN}/{method}"
    with urllib.request.urlopen(url, urllib.parse.urlencode(params).encode()) as r:
        payload = json.loads(r.read())
    if not payload["ok"]:
        raise RuntimeError(payload["description"])
    return payload["result"]


offset = 0
while True:
    for update in api("getUpdates", offset=offset, timeout=30):
        offset = update["update_id"] + 1
        # TODO проверять явно согласно документации какие есть в JSON поля
        api(
            "sendMessage",
            chat_id=update["message"]["chat"]["id"],
            text=update["message"]["text"],
        )
        print(".")
