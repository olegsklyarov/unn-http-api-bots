#!/usr/bin/env python3
"""Прибавить 1 к счётчику в JSON. Файл заблокирован на всё чтение и запись."""

import fcntl
import json
import sys

PATH = "data/counter.json"
COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 1

for _ in range(COUNT):
    with open(PATH, "r+") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        data = json.load(f)
        data["n"] += 1
        f.seek(0)
        f.truncate()
        json.dump(data, f)
        f.flush()
        fcntl.flock(f, fcntl.LOCK_UN)
