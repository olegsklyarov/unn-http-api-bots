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
