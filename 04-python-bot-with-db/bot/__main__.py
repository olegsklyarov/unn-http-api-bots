import time

import bot.database_client
import bot.telegram_api_client


def get_next_offset(updates: dict) -> int:
    next_offset = 0
    for update in updates:
        next_offset = max(next_offset, update["update_id"] + 1)
    return next_offset


def main() -> None:
    try:
        updates_next_offset = 0
        while True:
            updates = bot.telegram_api_client.get_updates(updates_next_offset)
            bot.database_client.persist_updates(updates)
            updates_next_offset = get_next_offset(updates)
            for update in updates:
                bot.telegram_api_client.send_message(
                    chat_id=update["message"]["chat"]["id"],
                    text=update["message"]["text"],
                )
                print(".", end="", flush=True)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
