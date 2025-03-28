#!/usr/bin/env python3
import psutil
print(f"{"Cpu Percent".ljust(10)} : {psutil.cpu_percent(interval=1)}")