import json
import os
import urllib.parse
import urllib.request

BASE_URL = os.environ["BASE_URL"]
TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]


def api_request(method, **params):
    url = f"{BASE_URL}/bot{TELEGRAM_TOKEN}/{method}"
    data = urllib.parse.urlencode(params).encode()
    with urllib.request.urlopen(url, data=data) as r:
        payload = json.loads(r.read())
    assert payload["ok"] == True, payload["description"]
    return payload


def get_updates(**params):
    return api_request("getUpdates", **params)["result"]


def send_message(**params):
    return api_request("sendMessage", **params)


def main():
    next_update_id = 0
    while True:
        for update in get_updates(offset=next_update_id, timeout=30):
            next_update_id = max(next_update_id, update["update_id"] + 1)
            # TODO проверять явно согласно документации какие есть в JSON поля
            send_message(
                chat_id=update["message"]["chat"]["id"],
                text=update["message"]["text"],
            )
            print(".", end="", flush=True)


if __name__ == "__main__":
    main()
