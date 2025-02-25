# @authur: Hench Wu, NetID:hhw14
# Rutgers University 
# CS419 Project 1-sbencrypt.py
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

def permutations_exchange(plaintext, keys, block_size):
    for i in range(block_size):
        first = keys[i] & 0x0f
        second = (keys[i] >> 4) & 0x0f
        plaintext[first], plaintext[second] = plaintext[second], plaintext[first]

if len(sys.argv) != 4:
    print(f"Usage: {sys.argv[0]} password plaintext ciphertext")
    sys.exit(1)
key_seed=sdbm(bytes(sys.argv[1], 'utf-8'))
with open(sys.argv[2], 'rb') as infile, open(sys.argv[3], 'wb') as outfile:
    block_size = 16
    prev_cipher = []
    for _ in range(block_size):
        key_seed=LCG(key_seed)
        prev_cipher.append(key_seed)
    while 1:
        in_plaintext = infile.read(4096)
        print(not in_plaintext)
        if not in_plaintext:
            break
        ciphertext = bytearray()
        n = len(in_plaintext)
        if n % block_size != 0:
            size_of_pad = block_size - (n % block_size)
            in_plaintext += bytes([size_of_pad] * size_of_pad)
            n += size_of_pad
        for i in range(0, n, block_size):
            block = list(in_plaintext[i:i + block_size])
            new_block = [block[i] ^ prev_cipher[i] for i in range(block_size)]
            keys = []
            for _ in range(block_size):
                key_seed=LCG(key_seed)
                keys.append(key_seed)
            permutations_exchange(new_block, keys, block_size)
            prev_cipher = [new_block[i] ^ keys[i] for i in range(block_size)]
            ciphertext.extend(prev_cipher)
        outfile.write(ciphertext)
