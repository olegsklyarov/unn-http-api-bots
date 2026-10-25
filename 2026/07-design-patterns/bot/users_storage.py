"""Актуальное состояние пользователей в data/users.json.

Достаём User из Update по типу payload; upsert с created_at / updated_at.
https://core.telegram.org/bots/api#user
https://docs.python.org/3/library/json.html
"""

import json
import time
from pathlib import Path

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
