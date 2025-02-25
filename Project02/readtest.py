
with open('log.txt', 'r') as file:
    head_hash = file.read().strip()
    print(head_hash)
    hash_list = head_hash.split('\n')
    print(hash_list)