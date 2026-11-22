#!/usr/bin/env python3
"""Прибавить 1 к счётчику в SQLite. Второй процесс ждёт, а не затирает значение."""

import sqlite3
import sys

PATH = "data/counter.db"
COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 1

# timeout: ждать, если базу сейчас пишет другой процесс.
conn = sqlite3.connect(PATH, timeout=30)
conn.execute("PRAGMA journal_mode=WAL")
conn.execute("PRAGMA synchronous=NORMAL")
for _ in range(COUNT):
    conn.execute("UPDATE counter SET n = n + 1 WHERE id = 1")
    conn.commit()
conn.close()
