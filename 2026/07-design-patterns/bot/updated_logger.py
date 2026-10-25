"""Локальный лог входящих Update на диск (data/updates/).

Отделён от цикла/handlers — separation of concerns через модуль.
https://docs.python.org/3/tutorial/modules.html
https://docs.python.org/3/library/json.html
Update: https://core.telegram.org/bots/api#update
"""

import json
from pathlib import Path


def persist_update(update):
    updates_dir = Path("data/updates")
    updates_dir.mkdir(parents=True, exist_ok=True)
    path = updates_dir / f"{update['update_id']}.json"
    path.write_text(
        json.dumps(update, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
