# logger.py

import datetime

def log_access(ip_address):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp}: Access from {ip_address}"
    write_to_log(log_entry)

def log_file_upload(ip_address, filename):
    timestamp = datetime.datetime.now()
    log_entry = f"{timestamp}: {ip_address} uploaded file {filename}"
    write_to_log(log_entry)

def write_to_log(log_entry):
    with open('access_log.txt', 'a') as log_file:
        log_file.write(log_entry + '\n')
