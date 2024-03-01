# logger.py

import os
import datetime

LOGS_DIRECTORY = 'static/data/logs'

def log_access(ip_address, action):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp}: {action} from {ip_address}"
    write_to_log(log_entry)

def log_file_upload(ip_address, filename):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp}: {ip_address} uploaded file {filename}"
    write_to_log(log_entry)

def write_to_log(log_entry):
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    log_file_path = os.path.join(LOGS_DIRECTORY, f'log_{current_date}.log')

    # Create logs directory if it doesn't exist
    if not os.path.exists(LOGS_DIRECTORY):
        os.makedirs(LOGS_DIRECTORY)

    with open(log_file_path, 'a') as log_file:
        log_file.write(log_entry + '\n')
