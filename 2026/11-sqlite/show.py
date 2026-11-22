#!/usr/bin/env python3
"""Показать счётчик: python3 show.py json|sqlite "заголовок" expected"""

import json
import sqlite3
import sys

kind, title, expected = sys.argv[1], sys.argv[2], int(sys.argv[3])
if kind == "json":
    n = json.load(open("data/counter.json"))["n"]
else:
    n = sqlite3.connect("data/counter.db").execute(
        "SELECT n FROM counter WHERE id = 1"
    ).fetchone()[0]
print(f"{title}: ожидалось {expected}, получилось {n}")
