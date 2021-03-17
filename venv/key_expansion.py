from sbox_table import AES_sbox

Rcon = [0x00000000, 0x01000000, 0x02000000,
        0x04000000, 0x08000000, 0x10000000,
        0x20000000, 0x40000000, 0x80000000,
        0x1b000000, 0x36000000]


def keyExpansion(key):

    round_keys = [()] * 44

    # Extract first 4 words for 1st round
    for i in range(4):
       round_keys[i] = (key[4 * i], key[4 * i + 1], key[4 * i + 2], key[4 * i + 3])

    # Extract rest words for other rounds
    for i in range(4, 44):

        # get 1st and last words
        temp = round_keys[i - 1]
        word = round_keys[i - 4]

        if i % 4 == 0:
            x = RotWord(temp)
            y = SubWord(x)
            rcon = Rcon[i // 4]

            temp = xor(y, hex(rcon)[2:])

        # Make strings to xor the values
        word = ''.join(word)
        temp = ''.join(temp)

        # xor the two hex values
        xord = xor(word, temp)
        round_keys[i] = (xord[:2], xord[2:4], xord[4:6], xord[6:8])

    return round_keys


def xor(value1, value2):
    xor = hex(int(hex2binary(value1), 2) ^ int(hex2binary(value2), 2))[2:]

    xor = '0' + xor if len(xor) != 8 else xor

    return xor


def hex2binary(hex):
    return bin(int(str(hex), 16))


def RotWord(word):
    return word[1:] + word[:1]


def SubWord(word):
    sWord = ()

    for i in range(4):

        # Covert hex to binary for 1st char
        if word[i][0].isdigit() == False:
            row = ord(word[i][0]) - 86
        else:
            row = int(word[i][0]) + 1

        

        # Covert hex to binary for 2nd char
        if word[i][1].isdigit() == False:
            col = ord(word[i][1]) - 86
        else:
            col = int(word[i][1]) + 1

        # get the index base on row and col (16x16 grid)
        sBoxIndex = (row * 16) - (17 - col)

        # get the value from sbox without prefix
        piece = hex(AES_sbox[sBoxIndex])[2:]

        # check length to ensure leading 0s are not forgotton
        if len(piece) != 2:
            piece = '0' + piece

        # form tuple
        sWord = (*sWord, piece)

    # return string
    return ''.join(sWord)


# def main():
#     
#     
#     key = ["0f", "15", "71", "c9", "47", "d9", "e8", "59", "0c", "b7", "ad", "d6", "af", "7f", "67", "98"]
# 
#     # expand key
#     w = keyExpansion(key)
# 
# if __name__ == '__main__':
#     main()