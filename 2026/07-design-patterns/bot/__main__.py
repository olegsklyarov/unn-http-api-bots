import json
import os
import urllib.parse
import urllib.request
from pathlib import Path

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


def persist_update(update):
    updates_dir = Path("data/updates")
    updates_dir.mkdir(parents=True, exist_ok=True)
    path = updates_dir / f"{update['update_id']}.json"
    path.write_text(
        json.dumps(update, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def main():
    next_update_id = 0
    try:
        while True:
            for update in get_updates(offset=next_update_id, timeout=30):
                next_update_id = max(next_update_id, update["update_id"] + 1)
                persist_update(update)
                # TODO проверять явно согласно документации какие есть в JSON поля
                send_message(
                    chat_id=update["message"]["chat"]["id"],
                    text=update["message"]["text"],
                )
                print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
