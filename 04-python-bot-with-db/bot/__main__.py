import json
import os
import sqlite3
import time
import urllib.request

from dotenv import load_dotenv

load_dotenv()


def make_request(method: str, **kwargs) -> dict:
    json_data = json.dumps(kwargs).encode('utf-8')

    request = urllib.request.Request(
        method='POST',
        url=f"{os.getenv("TELEGRAM_BASE_URI")}/{method}",
        data=json_data,
        headers={
            'Content-Type': 'application/json',
        },
    )

    with urllib.request.urlopen(request) as response:
        response_body = response.read().decode('utf-8')
        response_json = json.loads(response_body)
        assert response_json["ok"] == True
        return response_json["result"]


def get_updates(offset: int) -> dict:
    return make_request("getUpdates", offset=offset)


def send_message(chat_id: int, text: str) -> dict:
    return make_request("sendMessage", chat_id=chat_id, text=text)


def get_next_offset(updates: dict) -> int:
    next_offset = 0
    for update in updates:
        next_offset = max(next_offset, update["update_id"] + 1)
    return next_offset


def persist_updates(updates: dict) -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH"))
    with connection:
        data = []
        for update in updates:
            data.append((json.dumps(update),))
        connection.executemany("INSERT INTO telegram_events (payload) VALUES (?)", data)


def main() -> None:
    try:
        updates_next_offset = 0
        while True:
            updates = get_updates(updates_next_offset)
            persist_updates(updates)
            updates_next_offset = get_next_offset(updates)
            for update in updates:
                send_message(
                    chat_id=update["message"]["chat"]["id"],
                    text=update["message"]["text"],
                )
                print(".", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
