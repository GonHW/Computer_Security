# Hench Wu (hhw14) CS419 Project2 checklog

import os
import sys
import hashlib
import base64

def create_hash(input_string):
    hash_bytes = hashlib.sha256(input_string.encode()).digest()
    base64_hash = base64.b64encode(hash_bytes).decode()
    return base64_hash

# Function to check the integrity of the log file
def check_log():
    LOG_FILE_NAME = 'log.txt'
    HEAD_FILE_NAME = 'loghead.txt'
    # Check for the existence of log.txt and loghead.txt
    if not os.path.isfile(LOG_FILE_NAME):
        print("failed: log file is missing")
        sys.exit(1)
    if not os.path.isfile(HEAD_FILE_NAME):
        print("failed: head pointer file is missing")
        sys.exit(1)
        
    with open(HEAD_FILE_NAME, 'r') as head_file:
        head_hash = head_file.read().strip('\n')

    with open(LOG_FILE_NAME, 'r') as log_file:
        previous_hash = 'begin'
        line_number = 1        
        for line in log_file:
    
            # Remove the newline character from the line for hashing
            line = line.rstrip('\n')
            parts = line.split()
            if len(line) == 0 and line_number == 1:
                print(f"failed: lack of a starting line {line_number}")
                sys.exit(1)
            if len(line) == 0 and line_number != 1:
                print(f"failed: lack of line {line_number}. Corruption at line {line_number - 1}")
                sys.exit(1)
            
            if len(parts) < 4:
                print(f"failed: improper format at line {line_number}")
                sys.exit(1)
            current_hash = parts[3]
            parts2 = line.split(current_hash+' ')
            if len(parts2) == 1:
                log_entry = ''
            else: 
                log_entry = parts2[1]
            # print(f'{previous_hash} == {current_hash}')
            if previous_hash != current_hash:
                if line_number - 1 == 0 and 'begin' not in parts:
                    print(f"failed: corruption at line {line_number} (hash 'begin' corrupted)")
                else:
                    i = 1
                    if line_number == 1:
                        i = 0    
                    print(f"failed: corruption at line {line_number - i}")
                sys.exit(1)
            previous_hash = create_hash(f"{parts2[0]}{previous_hash} {log_entry}")
            line_number += 1
            
        if head_hash != previous_hash:
            i = 1
            if line_number == 1:
                i = 0    
            print(f"failed: corruption at line {line_number - i}")
            sys.exit(1)

    # If all lines match up, the log is valid
    print("valid")
    sys.exit(0)

if len(sys.argv) > 1:
    print("Usage: checklog")
    sys.exit(1)
check_log()
