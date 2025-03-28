#!/usr/bin/env python3
import psutil
print(f"{"Disk Usage".ljust(10)} : {psutil.disk_usage('/').percent}")