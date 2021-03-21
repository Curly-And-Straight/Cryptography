from Crypto.Util.number import bytes_to_long
from Crypto.Random import get_random_bytes
import Crypto
import libnum
import math
import random
import json

bits = 2048

print("Please enter your plaintext path...")
path = input()

with open(path, 'r') as file:
    msg = file.read()

print("Keys are generating...")

p = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
q = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)

while p == q:
    p = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)
    q = Crypto.Util.number.getPrime(bits, randfunc=get_random_bytes)

n = p * q
PHI = (p - 1) * (q - 1)

e = random.randint(2, PHI - 1)

while math.gcd(e, PHI) != 1:
    e = random.randint(2, PHI - 1)

d = libnum.invmod(e, PHI)

print("Keys generated.")
message = bytes_to_long(msg.encode('utf-8'))

cipher = pow(message, d, n)

with open(path.split('/')[:-1] + "cipher.json", 'w') as file:
    data = {'cipher': cipher, 'public_key': (e, n)}
    json.dump(data, file)

print("The ciphertext and public key are saved to {}/cipher.json".format(path.split('/')[:-1]))
