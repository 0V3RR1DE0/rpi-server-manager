# network_logs.py

import datetime

def log_access(ip_address, action):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"{timestamp}: {action} from {ip_address}"
    write_to_log(log_entry)

def write_to_log(log_entry):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = f'static/data/logs/log_{current_date}.log'
    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')

def get_network_logs():
    logs = []
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = f'static/data/logs/log_{current_date}.log'
    with open(log_file_path, 'r') as log_file:
        for line in log_file:
            logs.append(line.strip())  # Append each line of the log file as it is
    return logs
