import hashlib
import base64

# Input string
input_string = "Hello, world!"

# Calculate SHA-256 hash of the input string
hash_bytes = hashlib.sha256(input_string.encode()).digest()

# Convert the SHA-256 hash to Base64
base64_hash = base64.b64encode(hash_bytes).decode()

print("Input text: " + input_string)
print("Base64 Encoded SHA256 Hash: " + base64_hash)

