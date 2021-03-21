import json

from Crypto.Util.number import long_to_bytes
from functions import *
from sbox_table import *


def dec(key, data):

    grids = break_in_grids_of_16(data)
    expanded_key = expand_key(key, 11)
    temp_grids = []
    round_key = extract_key_for_round(expanded_key, 10)

    temp_grids = []

    for grid in grids:

        add_sub_key_step = add_sub_key(grid, round_key)
        shift_rows_step = [rotate_row_left(
            add_sub_key_step[i], -1 * i) for i in range(4)]
        sub_bytes_step = [[reverse_lookup(val) for val in row]
                          for row in shift_rows_step]
        temp_grids.append(sub_bytes_step)

    grids = temp_grids

    for round in range(9, 0, -1):
        temp_grids = []

        for grid in grids:
            round_key = extract_key_for_round(expanded_key, round)
            add_sub_key_step = add_sub_key(grid, round_key)

            mix_column_step = mix_columns(add_sub_key_step)
            mix_column_step = mix_columns(mix_column_step)
            mix_column_step = mix_columns(mix_column_step)
            shift_rows_step = [rotate_row_left(
                mix_column_step[i], -1 * i) for i in range(4)]
            sub_bytes_step = [
                [reverse_lookup(val) for val in row] for row in shift_rows_step]
            temp_grids.append(sub_bytes_step)

        grids = temp_grids
        temp_grids = []

    round_key = extract_key_for_round(expanded_key, 0)

    for grid in grids:
        temp_grids.append(add_sub_key(grid, round_key))

    grids = temp_grids

    int_stream = []
    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_stream.append(grid[row][column])

    return bytes(int_stream)


if __name__ == '__main__':
    print("Please enter your ciphertext name...")
    name = input()

    with open(name) as file:
        data = json.load(file)
        cipher = long_to_bytes(data['cipher'])
        key = data['key']


    converted_key = []
    [converted_key.append(ele) for ele in key.encode()]

    decrypt = dec(converted_key, cipher)

    decrypt = decrypt.decode('utf-8')
    decrypt = decrypt.rstrip('\0')

    with open('AES_decrypted', 'w') as file:
        file.write(decrypt)
    print("The plaintext saved in AES_decrypted")
