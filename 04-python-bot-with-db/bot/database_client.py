import json
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()


def persist_updates(updates: dict) -> None:
    connection = sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH"))
    with connection:
        data = []
        for update in updates:
            data.append((json.dumps(update),))
        connection.executemany("INSERT INTO telegram_events (payload) VALUES (?)", data)
