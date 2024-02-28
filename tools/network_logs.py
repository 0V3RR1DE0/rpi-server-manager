# network_logs.py

import os
from datetime import datetime

def get_network_logs():
    """Read logs from the file and return them."""
    log_file_path = generate_log_file_path()
    with open(log_file_path, 'r') as file:
        logs = file.readlines()
    return logs

def generate_log_file_path():
    """Generate the path to the logs file."""
    current_date_time = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    return f'static/data/logs/log_{current_date_time}.log'
