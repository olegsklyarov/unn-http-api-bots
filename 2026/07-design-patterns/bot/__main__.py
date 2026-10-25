import json
import os
import time
import urllib.parse
import urllib.request
from pathlib import Path

TOKEN = os.environ["TELEGRAM_TOKEN"]

USERS_PATH = Path("data/users.json")

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


def persist_update(update):
    updates_dir = Path("data/updates")
    updates_dir.mkdir(parents=True, exist_ok=True)
    path = updates_dir / f"{update['update_id']}.json"
    path.write_text(
        json.dumps(update, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


def user_from_update(update):
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


def _dump_users(users):
    items = sorted(users.items(), key=lambda kv: kv[0])
    lines = ["{"]
    for i, (uid, record) in enumerate(items):
        body = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'  "{uid}": {body}{comma}')
    lines.append("}")
    return "\n".join(lines) + "\n"


def persist_user(update):
    user = user_from_update(update)
    if user is None:
        return
    user_id = int(user["id"])
    now = int(time.time())

    USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    if USERS_PATH.exists():
        users = {
            int(k): v
            for k, v in json.loads(USERS_PATH.read_text(encoding="utf-8")).items()
        }
    else:
        users = {}

    if user_id in users:
        created_at = users[user_id]["created_at"]
        users[user_id] = {**user, "created_at": created_at, "updated_at": now}
    else:
        users[user_id] = {**user, "created_at": now, "updated_at": now}

    USERS_PATH.write_text(_dump_users(users), encoding="utf-8")


def main():
    next_update_id = 0
    try:
        while True:
            for update in get_updates(offset=next_update_id, timeout=30):
                next_update_id = max(next_update_id, update["update_id"] + 1)
                persist_update(update)
                persist_user(update)
                message = update.get("message")
                if message is None:
                    continue
                chat_id = message["chat"]["id"]
                if "text" in message:
                    send_message(chat_id=chat_id, text=message["text"])
                elif "sticker" in message:
                    send_sticker(
                        chat_id=chat_id,
                        sticker=message["sticker"]["file_id"],
                    )
                elif "video_note" in message:
                    send_video_note(
                        chat_id=chat_id,
                        video_note=message["video_note"]["file_id"],
                    )
                else:
                    continue
                print(".", end="", flush=True)
    except KeyboardInterrupt:
        print("\nBye!")


if __name__ == "__main__":
    main()
