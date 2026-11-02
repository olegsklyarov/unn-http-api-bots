import copy
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


def default_state():
    return {
        "current_state": "waiting_for_recipe",
        "order_content": {
            "recipe": None,
            "size": None,
            "crust": None,
            "drink": None,
        },
    }


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


def user_id_from_update(update):
    user = user_from_update(update)
    if user is None:
        return None
    return int(user["id"])


def _load_users():
    if not USERS_PATH.exists():
        return {}
    return {
        int(k): v
        for k, v in json.loads(USERS_PATH.read_text(encoding="utf-8")).items()
    }


def _dump_users(users):
    items = sorted(users.items(), key=lambda kv: kv[0])
    lines = ["{"]
    for i, (uid, record) in enumerate(items):
        body = json.dumps(record, ensure_ascii=False, separators=(",", ":"))
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'  "{uid}": {body}{comma}')
    lines.append("}")
    return "\n".join(lines) + "\n"


def _write_users(users):
    USERS_PATH.parent.mkdir(parents=True, exist_ok=True)
    USERS_PATH.write_text(_dump_users(users), encoding="utf-8")


def get_user_state(user_id):
    users = _load_users()
    record = users.get(int(user_id))
    if record is None or "state" not in record:
        return default_state()
    return copy.deepcopy(record["state"])


def save_user_state(user_id, state):
    user_id = int(user_id)
    users = _load_users()
    now = int(time.time())
    if user_id not in users:
        users[user_id] = {
            "id": user_id,
            "created_at": now,
            "updated_at": now,
            "state": copy.deepcopy(state),
        }
    else:
        users[user_id] = {
            **users[user_id],
            "state": copy.deepcopy(state),
            "updated_at": now,
        }
    _write_users(users)


def persist_user(update):
    user = user_from_update(update)
    if user is None:
        return
    user_id = int(user["id"])
    now = int(time.time())

    users = _load_users()

    if user_id in users:
        existing = users[user_id]
        created_at = existing["created_at"]
        state = existing.get("state", default_state())
        users[user_id] = {
            **user,
            "created_at": created_at,
            "updated_at": now,
            "state": state,
        }
    else:
        users[user_id] = {
            **user,
            "created_at": now,
            "updated_at": now,
            "state": default_state(),
        }

    _write_users(users)
