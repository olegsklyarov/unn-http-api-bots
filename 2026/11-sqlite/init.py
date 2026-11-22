#!/usr/bin/env python3
"""Создать пустой счётчик: python3 init.py json|sqlite"""

import os
import shutil
import sqlite3
import sys

os.makedirs("data", exist_ok=True)
shutil.rmtree("data")
os.makedirs("data")

kind = sys.argv[1]
if kind == "json":
    open("data/counter.json", "w").write('{"n": 0}\n')
elif kind == "sqlite":
    conn = sqlite3.connect("data/counter.db")
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("CREATE TABLE counter (id INTEGER PRIMARY KEY, n INTEGER)")
    conn.execute("INSERT INTO counter VALUES (1, 0)")
    conn.commit()
    conn.close()
else:
    raise SystemExit("нужно: json или sqlite")
