# Hench Wu (hhw14) CS419 Project2 addlog

import os
import sys
import hashlib
import base64
from datetime import datetime

# Function to get the hash of the last line in the log file
def get_last_line_hash(log_file_name, head_file_name):
    if not os.path.isfile(head_file_name):
        print("Error: The head pointer file is missing.")
        sys.exit(1)
    else:
        with open(head_file_name, 'r') as head_file:
            head_hash = head_file.read().strip("\n")
            if head_hash == '' and os.stat(log_file_name).st_size == 0:
                return 'begin'
            return head_hash

# Function to create a base-64 encoded SHA-256 hash of the input string
def create_hash(input_string):
    hash_bytes = hashlib.sha256(input_string.encode()).digest()
    base64_hash = base64.b64encode(hash_bytes).decode()
    return base64_hash

# Function to add a log entry
def add_log_entry(log_string):
    LOG_FILE_NAME = 'log.txt'
    HEAD_FILE_NAME = 'loghead.txt'
    # Replace newline characters in the user-supplied string with spaces
    log_string = log_string.replace('\n', ' ')
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # If log.txt does not exist, ignore loghead.txt (if it exists), create a new log file,
    # then create loghead.txt to contain the hash of the newly-added log entry
    if not os.path.isfile(LOG_FILE_NAME):
        # If log.txt is missing, we start a new chain with "begin"
        previous_hash = 'begin'
    else:
        previous_hash = get_last_line_hash(LOG_FILE_NAME, HEAD_FILE_NAME)
    
    # Create the log entry string
    log_entry = f"{timestamp} - {previous_hash} {log_string}\n"
    
    with open(LOG_FILE_NAME, 'a') as log_file:
        log_file.write(log_entry)
    
    new_hash = create_hash(log_entry.rstrip('\n'))
    with open(HEAD_FILE_NAME, 'w') as head_file:
        head_file.write(new_hash)


if len(sys.argv) != 2 :
    print("Usage: addlog log_string")
    sys.exit(1)
log_string = sys.argv[1]
add_log_entry(log_string)
print("Log entry added successfully.")

