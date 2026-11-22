#!/usr/bin/env python3
"""Прибавить 1 к счётчику в JSON. Блокировки нет, обновления теряются."""

import json
import os
import sys

PATH = "data/counter.json"
COUNT = int(sys.argv[1]) if len(sys.argv) > 1 else 1

for _ in range(COUNT):
    with open(PATH) as f:
        data = json.load(f)

    data["n"] += 1

    # Свой временный файл и подмена целиком: читатель не видит пустой JSON.
    # Потерянное обновление это не лечит — n уже прочитан.
    tmp = f"{PATH}.{os.getpid()}"
    with open(tmp, "w") as f:
        json.dump(data, f)
    os.replace(tmp, PATH)
