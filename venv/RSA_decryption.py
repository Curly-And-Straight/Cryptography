from Crypto.Util.number import long_to_bytes, bytes_to_long
import json

print("Please enter your ciphertext path...")
path = input()

with open(path) as file:
    data = json.load(file)
    cipher = data.cipher
    e = data.public_key[0]
    n = data.public_key[1]


res = pow(cipher, e, n)
decrypt = long_to_bytes(res).decode()

with open(path.split('/')[:-1] + "plaintext.txt", 'w') as file:
    file.write(decrypt)