import json
import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()


def persist_update(update: dict) -> None:
    payload = json.dumps(update, ensure_ascii=False)
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            connection.execute("INSERT INTO telegram_events (payload) VALUES (?)", (payload,))


def recreate_database() -> None:
    with sqlite3.connect(os.getenv('SQLITE_DATABASE_PATH')) as connection:
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
