#!/usr/bin/env python3
import psutil
print(f"{"Process Count".ljust(10)} : {len(psutil.pids())}")