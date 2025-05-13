import json
from pprint import pprint

def sys_info():
    """
    Returns system information including OS, CPU, and memory details.
    """
    import platform
    import psutil

    # Get OS information
    os_info = platform.uname()._asdict()

    # Get CPU information
    cpu_info = {
        'Physical cores': psutil.cpu_count(logical=False),
        'Total cores': psutil.cpu_count(logical=True),
        'Max Frequency': f"{psutil.cpu_freq().max}MHz",
        'Min Frequency': f"{psutil.cpu_freq().min}MHz",
        'Current Frequency': f"{psutil.cpu_freq().current}MHz",
        'CPU Usage': f"{psutil.cpu_percent(interval=1)}%"
    }

    # Get memory information
    memory_info = {
        'Total Memory': f"{round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB",
        'Available Memory': f"{round(psutil.virtual_memory().available / (1024 ** 3), 2)} GB",
        'Used Memory': f"{round(psutil.virtual_memory().used / (1024 ** 3), 2)} GB",
        'Memory Usage': f"{psutil.virtual_memory().percent}%"
    }

    return {
        'OS Information': os_info,
        'CPU Information': cpu_info,
        'Memory Information': memory_info
    }

# === Run it and save to .txt ===

info = sys_info()

with open("system_info.txt", "w") as f:
    f.write(json.dumps(info, indent=4))

print("[+] System info written to system_info.txt")
