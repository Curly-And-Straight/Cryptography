from AES_encryption import encryption

# key = [0x0f, 0x15, 0x71, 0xc9, 0x47, 0xd9, 0xe8, 0x59, 0x0c, 0xb7, 0xad, 0xd6, 0xaf, 0x7f, 0x67, 0x98]
key = ["0f", "15", "71", "c9", "47", "d9", "e8", "59", "0c", "b7", "ad", "d6", "af", "7f", "67", "98"]

if __name__ == '__main__':

    input = 'Hello world'

    cipher = encryption(bytes(input, 'utf-8'), key=key)
    print(cipher)

