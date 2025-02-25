# @authur: Hench Wu, NetID:hhw14
# Rutgers University 
# CS419 Project 1-scrypt.py
import sys

def LCG(Xn):
    m, a, c = 256, 1103515245, 12345
    return (a * Xn + c) % m

def sdbm(str=""):
    c, hash = 0, 0
    while(len(str) > c):
        hash = ord(str[c]) + (hash << 6) + (hash << 16) - hash
        c+=1
    return hash
cmdline = sys.argv[1:]
if len(cmdline) != 3:
    info = f'{sys.argv[0]} password'
    print(f"Usage: {info} plaintext ciphertext\n\tor\n{info} ciphertext plaintext")
    sys.exit(1)
seed = sdbm(cmdline[0])
try:
    with open(cmdline[1], "rb") as input, open(cmdline[2],"wb") as output:
        while 1 :
            in_text = list(input.read(4096))
            if not in_text:
                break
            key = seed
            out_text = bytearray()
            for byte in in_text:
                key = LCG(key)
                out_text.append((byte ^ key))
            output.write(out_text)             
except Exception as e:
    print("Error: ", e)
    sys.exit(1)
            