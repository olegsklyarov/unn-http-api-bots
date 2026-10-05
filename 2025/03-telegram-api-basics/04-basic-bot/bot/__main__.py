import time

import requests

from bot.config_reader import env_config


def main() -> None:
    token = env_config.telegram_token.get_secret_value()

    def send_message(chat_id: int, text: str) -> None:
        params = {
            "chat_id": chat_id,
            "text": text,
        }
        response = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            params=params,
        )
        response_json = response.json()
        assert response_json["ok"] == True

    def get_updates() -> dict:
        nonlocal next_update_id
        params = {
            "offset": next_update_id,
        }
        response = requests.post(
            f"https://api.telegram.org/bot{token}/getUpdates",
            params=params,
        )
        response_json = response.json()
        assert response_json["ok"] == True

        updates = response_json["result"]
        for update in updates:
            next_update_id = max(next_update_id, update["update_id"] + 1)

        return updates

    try:
        next_update_id = 0
        while True:
            for update in get_updates():
                send_message(update["message"]["chat"]["id"], update["message"]["text"])
                print(".", end="", flush=True)

            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
