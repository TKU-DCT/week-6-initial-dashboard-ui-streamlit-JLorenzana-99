import psutil
from datetime import datetime
import csv
import os
import time
import subprocess
import platform

def get_system_info():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cpu = psutil.cpu_percent(interval=1)
    memory = psutil.virtual_memory().percent
    disk = psutil.disk_usage('/').percent
    ping_status, ping_ms = ping_host("8.8.8.8")
    return [now, cpu, memory, disk, ping_status, ping_ms]

def ping_host(host):
    try:
        # Handle cross-platform ping command
        param = "-n" if platform.system().lower() == "windows" else "-c"
        output = subprocess.check_output(["ping", param, "1", host], stderr=subprocess.DEVNULL).decode()
        ms = parse_ping_time(output)
        return ("UP", ms)
    except:
        return ("DOWN", -1)

def parse_ping_time(output):
    for line in output.splitlines():
        if "time=" in line:
            parts = line.split("time=")
            if len(parts) > 1:
                try:
                    return float(parts[1].split()[0])
                except ValueError:
                    return -1
    return -1

def write_log(data):
    file_exists = os.path.isfile("log.csv")
    with open("log.csv", "a", newline='') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "CPU", "Memory", "Disk", "Ping_Status", "Ping_ms"])
        writer.writerow(data)

if __name__ == "__main__":
    for _ in range(5):
        row = get_system_info()
        write_log(row)
        print("Logged:", row)
        time.sleep(10)
