import json
import random
import string

from Crypto.Util.number import bytes_to_long
from functions import *
from sbox_table import *


def enc(key, data):
    pad = bytes(16 - len(data) % 16)

    if len(pad) != 16:
        data += pad
    grids = break_in_grids_of_16(data)

    expanded_key = expand_key(key, 11)

    temp_grids = []
    round_key = extract_key_for_round(expanded_key, 0)

    for grid in grids:
        temp_grids.append(add_sub_key(grid, round_key))

    grids = temp_grids

    for round in range(1, 10):
        temp_grids = []

        for grid in grids:
            sub_bytes_step = [[lookup(val) for val in row] for row in grid]
            shift_rows_step = [rotate_row_left(
                sub_bytes_step[i], i) for i in range(4)]
            mix_column_step = mix_columns(shift_rows_step)
            round_key = extract_key_for_round(expanded_key, round)
            add_sub_key_step = add_sub_key(mix_column_step, round_key)
            temp_grids.append(add_sub_key_step)

        grids = temp_grids

    temp_grids = []
    round_key = extract_key_for_round(expanded_key, 10)

    for grid in grids:
        sub_bytes_step = [[lookup(val) for val in row] for row in grid]
        shift_rows_step = [rotate_row_left(
            sub_bytes_step[i], i) for i in range(4)]
        add_sub_key_step = add_sub_key(shift_rows_step, round_key)
        temp_grids.append(add_sub_key_step)

    grids = temp_grids

    int_stream = []

    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_stream.append(grid[row][column])

    return bytes(int_stream)

if __name__ == '__main__':

    key = ''.join(random.choice(string.ascii_lowercase) for i in range(16))
    print(key)
    print("Please enter your plaintext name...")
    name = input()
    with open(name, 'r') as file:
        plain_text = file.read()

    converted_key = []
    [converted_key.append(ele) for ele in key.encode()]

    encrypt = enc(converted_key, bytes(plain_text, encoding='utf-8'))

    with open('AES_encrypted', 'w') as file:

        data = {'cipher': bytes_to_long(encrypt), 'key': key}
        json.dump(data, file)

    print("The ciphertext and key are saved to AES_encrypted")
