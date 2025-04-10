#!/usr/bin/env python3
import psutil
print(f"{psutil.cpu_percent(interval=1)}")