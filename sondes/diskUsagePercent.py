#!/usr/bin/env python3
import psutil
print(f"{psutil.disk_usage('/').percent}")