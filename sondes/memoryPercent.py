#!/usr/bin/env python3
import psutil
print(f"{"Memory Percent".ljust(10)} : {psutil.virtual_memory().percent}")