# @authur: Hench Wu, NetID:hhw14
# Rutgers University 
# CS419 Project 1-sbdecrypt.py
import sys

def sdbm(str=""):
    c, hash = 0, 0
    while(len(str) > c):
        hash = str[c] + (hash << 6) + (hash << 16) - hash
        c+=1
    return hash

def LCG(Xn):
    m, a, c = 256, 1103515245, 12345
    return (a * Xn + c) % m

def permutations_exchange(block, keys, block_size):
    for i in range(block_size - 1, -1, -1):
        first = keys[i] & 0x0f
        second = (keys[i] >> 4) & 0x0f
        block[first], block[second] = block[second], block[first]

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} password ciphertext plaintext")
    sys.exit(1)
key_seed=sdbm(bytes(sys.argv[1], 'utf-8'))
with open(sys.argv[2], 'rb') as infile, open(sys.argv[3], 'wb') as outfile:
    block_size = 16
    prev_ciphertext = []
    for _ in range(block_size):
        key_seed=LCG(key_seed)
        prev_ciphertext.append(key_seed)
    while 1:
        in_ciphertext = infile.read(4096)
        if not in_ciphertext:
            break
        plaintext = bytearray()
        n = len(in_ciphertext)
        for i in range(0, n, block_size):
            block = list(in_ciphertext[i:i + block_size])
            new_block = [0] * block_size
            keys = []
            for _ in range(block_size):
                key_seed=LCG(key_seed)
                keys.append(key_seed)
            for i in range(block_size):
                new_block[i] = block[i] ^ keys[i]
            permutations_exchange(new_block, keys, block_size)
            plaintext.extend([new_block[i] ^ prev_ciphertext[i] for i in range(block_size)])
            prev_ciphertext = block

        if len(in_ciphertext) < 4096:
            pad = plaintext[-1]
            plaintext = plaintext[:-pad]
        outfile.write(plaintext)

