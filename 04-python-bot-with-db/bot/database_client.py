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
            data.append((json.dumps(update, ensure_ascii=False),))
        connection.executemany("INSERT INTO telegram_events (payload) VALUES (?)", data)
    connection.close()


def recreate_database() -> None:
    connection = sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH'))
    with connection:
        connection.execute("DROP TABLE IF EXISTS telegram_events")
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS telegram_events
            (
                id INTEGER PRIMARY KEY,
                payload TEXT NOT NULL
            )
            """,
        )
    connection.close()
