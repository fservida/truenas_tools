#!/usr/local/bin/python
# Network Watchdog to reebot TrueNAS if Realtek card shits the bed
# Test connection every period seconds
# If connection down, try again after an exponential backoff period.
# If exceeded perform action (reboot box)

import subprocess
import time

# Settings
period = 30
monitor_ip = "172.21.20.1"
command = "reboot"
max_retry = 4
# End Settings

retry_count = 0

while True:
    res = subprocess.run(["ping", "-c 1", monitor_ip], capture_output=True)
    if not (res.returncode == 0):
        if retry_count >= max_retry:
            print(f"Connection Down and backoff period exceeded. Running '{command}' command now.")
            subprocess.run([command])
        backoff_time = period*(2**(retry_count))
        print(f"Connection Down! Backing off for {backoff_time} seconds.")
        time.sleep(backoff_time)
        retry_count += 1
    else:
        retry_count = 0
        time.sleep(period)
        