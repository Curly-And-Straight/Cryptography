from Crypto.Util.number import long_to_bytes, bytes_to_long
import json
import base64
print("Please enter your ciphertext name...")
name = input()

with open(name) as file:
    data = json.load(file)
    cipher = data['cipher']
    e = data['public_key'][0]
    n = data['public_key'][1]


res = pow(cipher, e, n)
decrypt = base64.b64decode(long_to_bytes(res)).decode('utf-8')

with open("RSA_decrypted", 'w') as file:
    file.write(decrypt)

print('Ciphertext decrypted and saved into RSA_decrypted')
