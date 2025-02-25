# @authur: Hench Wu, NetID:hhw14
# Rutgers University 
# CS419 Project 1-ctencrypt.py
import sys
import argparse
import math

def parse_key(key):
    indexed_chars = list(enumerate(key))
    sorted_pairs = sorted(indexed_chars, key=lambda x: x[1])
    real_key = [index for index, char in sorted_pairs]
    return real_key

def encrypt_block(block, key_order, rows, col):
    elist = []
    k = 0
    for i in range(col):
        for j in range(rows):
            if block[j][key_order[i]] == -1:
                break
            elist.append(block[j][key_order[i]])
    return elist

def encrypt_data(data, key = "ABCD", blocksize = 16):
    col = len(key)
    rows = math.ceil(blocksize / col)
    num_block = math.ceil(len(data) / blocksize)
    key_order = parse_key(key)
    countletter = 0
    grid = [[[-1 for _ in range(col)] for _ in range(rows)] for _ in range(num_block)]
    for i in range(num_block):
        counter = 0
        for j in range(rows):
            for k in range(col):
                grid[i][j][k] = data[countletter]
                counter += 1
                countletter += 1
                if not countletter < len(data) or counter >= blocksize:
                    break
            if not countletter < len(data) or counter >= blocksize:
                break
        if not countletter < len(data):
            break
    elist = []
    for i in range(num_block):
        block = grid[i]
        elist.extend(encrypt_block(block, key_order, rows, col))
    sys.stdout.buffer.write(bytes(elist))

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--blocksize', type=int, default=16, help='Block size (default: 16)')
parser.add_argument('-k', '--key', required=True, help='Encryption key')
parser.add_argument('input_file', type=argparse.FileType('rb'), help='File containing plaintext to encrypt')
args = parser.parse_args()

plaintext = args.input_file.read()
encrypt_data(plaintext, args.key, args.blocksize)
