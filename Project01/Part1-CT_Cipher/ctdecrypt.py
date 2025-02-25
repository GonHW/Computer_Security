# @authur: Hench Wu, NetID:hhw14
# Rutgers University 
# CS419 Project 1-ctdecrypt.py
import sys
import argparse
import math

def parse_key(key):
    indexed_chars = list(enumerate(key))
    sorted_pairs = sorted(indexed_chars, key=lambda x: x[1])
    real_key = [index for index, char in sorted_pairs]
    return real_key

def decrypt_block(block, key_order, rows, col):
    dlist = []
    for i in range(rows):
        for j in range(col):
            if block[i][j] == -1:
                break
            dlist.append(block[i][j])
    return dlist

def decrypt_data(data, key = "ABCD", blocksize = 12):
    col = len(key)
    rows = math.ceil(blocksize / col)
    # blocksize = rows * col
    pad = blocksize - len(data) % blocksize
    if pad == blocksize:
        pad = 0
    pad2 = rows * col - blocksize
    num_block = math.ceil(len(data) / blocksize)
    key_order = parse_key(key)
    grid = [[[0 for _ in range(col)] for _ in range(rows)] for _ in range(num_block)]
    for i in range(num_block-1):
        counter = 0
        r1 = rows - 1
        while pad2 > counter and r1 >= 0 :
            c1 = col - 1
            while pad2 > counter and c1 >= 0:
                grid[i][r1][c1] = -1
                c1 -= 1
                counter += 1
            r1 -= 1
    counter = 0
    r1 = rows - 1
    while num_block>0 and pad+pad2 > counter and r1 >= 0 :
        c1 = col - 1
        while pad+pad2 > counter and c1 >= 0:
            grid[num_block-1][r1][c1] = -1
            c1 -= 1
            counter += 1
        r1 -= 1
    counter = 0
    for i in range(num_block):
        for j in range(col):
            for k in range(rows):
                if grid[i][k][key_order[j]] != -1:
                    grid[i][k][key_order[j]] = data[counter]
                    counter += 1
                if not counter < len(data):
                    break
            if not counter < len(data):
                break
        if not counter < len(data):
            break
    dlist = []
    for i in range(num_block):
        block = grid[i]
        dlist.extend(decrypt_block(block, key_order, rows, col))
    sys.stdout.buffer.write(bytes(dlist))

parser = argparse.ArgumentParser()
parser.add_argument('-b', '--blocksize', type=int, default=16, help='Block size (default: 16)')
parser.add_argument('-k', '--key', required=True, help='Encryption key')
parser.add_argument('input_file', type=argparse.FileType('rb'), help='File containing plaintext to encrypt')
args = parser.parse_args()

ciphertext = args.input_file.read()
decrypt_data(ciphertext, args.key, args.blocksize)
