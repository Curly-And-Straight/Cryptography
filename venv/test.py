from AES_encryption import *
from AES_decryption import *



key = 'ArminSobhanCrypt'
plain_text = 'This is an AES enc/dec algorithm which is implemented from zero to 100 by A.Eftekhari and S.MoradianDaghigh'

if __name__ == '__main__':

    converted_key = []
    [converted_key.append(ele) for ele in key.encode()]

    encrypt = enc(converted_key, bytes(plain_text, encoding='utf-8'))
    decrypt = dec(converted_key, encrypt)

    decrypt = decrypt.decode('utf-8')
    decrypt = decrypt.rstrip('\0')

    print("PlainText:  ", plain_text)
    print("Key:        ", key)
    print("CipherText: ", encrypt)
    print("Final res:  ", decrypt)

