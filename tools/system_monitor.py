# system_monitor.py

from flask import render_template
import psutil

def get_system_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent

    # Get information about all disks
    disk_info = []
    for partition in psutil.disk_partitions():
        partition_info = {
            'drive': partition.device,
            'mountpoint': partition.mountpoint,
            'total_space': round(psutil.disk_usage(partition.mountpoint).total / (1024**3), 2),
            'used_space': round(psutil.disk_usage(partition.mountpoint).used / (1024**3), 2),
            'free_space': round(psutil.disk_usage(partition.mountpoint).free / (1024**3), 2),
        }
        disk_info.append(partition_info)

    return {'cpu_usage': cpu_usage, 'memory_usage': memory_usage, 'disk_info': disk_info}


def render_system_monitor():
    system_info = get_system_info()
    return render_template('system_monitor.html', system_info=system_info)
