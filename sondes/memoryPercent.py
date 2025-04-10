#!/usr/bin/env python3
import psutil
print(f"{psutil.virtual_memory().percent}")