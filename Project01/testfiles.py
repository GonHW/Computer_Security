def read_bytes(file_path):
    byte_read = 0
    with open(file_path, "rb") as file:
        file_bytes = file.read()
        byte_read = file.tell()
    return byte_read
def read_file(file_path):
    file_read = list()
    with open(file_path, "rb") as file:
        file_read = list(file.read())
    return list(file_read)


# Example usage
f_path1 = "en-clown.txt"
f_path2 = "en-clowncpu.txt"
f_bytes1 = read_bytes(f_path1)
f_bytes2 = read_bytes(f_path2)
f_list1 = read_file(f_path1)
f_list2 = read_file(f_path2)
print(f"f_bytes1:{f_bytes1} bytes\nf_bytes2:{f_bytes2} bytes\n{f_bytes1==f_bytes2} {f_list1==f_list2}")
