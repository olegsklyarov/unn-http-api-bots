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
            connection.execute("DROP TABLE IF EXISTS users")
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS telegram_events
                (
                    id INTEGER PRIMARY KEY,
                    payload TEXT NOT NULL
                )
                """,
            )
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS users
                (
                    id INTEGER PRIMARY KEY,
                    telegram_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    state TEXT DEFAULT NULL,
                    data TEXT DEFAULT NULL
                )
                """,
            )


def user_exists(telegram_id: int) -> bool:
    """Check if a user with the given telegram_id exists in the users table."""
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            cursor = connection.execute(
                "SELECT 1 FROM users WHERE telegram_id = ?", (telegram_id,)
            )
            return cursor.fetchone() is not None


def create_user(telegram_id: int) -> None:
    """Create a new user record in the users table."""
    with sqlite3.connect(os.getenv("SQLITE_DATABASE_PATH")) as connection:
        with connection:
            connection.execute(
                "INSERT INTO users (telegram_id) VALUES (?)", (telegram_id,)
            )
