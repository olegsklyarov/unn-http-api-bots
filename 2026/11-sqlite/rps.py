#!/usr/bin/env python3
"""Замерить RPS: python3 rps.py "имя" script.py N"""

import subprocess
import sys
import time

title, script, count = sys.argv[1], sys.argv[2], int(sys.argv[3])
started = time.perf_counter()
subprocess.check_call([sys.executable, script, str(count)])
elapsed = time.perf_counter() - started
print(f"{title}: {count} инкрементов за {elapsed:.3f} с — {count / elapsed:.0f} RPS")
