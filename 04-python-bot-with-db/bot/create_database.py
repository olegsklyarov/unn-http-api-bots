import os
import sqlite3

from dotenv import load_dotenv

load_dotenv()
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
