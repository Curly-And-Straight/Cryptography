import numpy as np
from sbox_table import AES_sbox, reverse_AES_sbox

def segmentation(input):
    for i in input:
        print("len:" ,i)

    segmented = []
    for i in range(len(input) // 16):
        box = input[i * 16: (i + 1) * 16]
        grid = [[], [], [], []]
        [grid[i].append(box[i + 4 * j]) for i in range(4) for j in range(4)]

        segmented.append(grid)

    print(segmented)

    return segmented


def lookup(value):
    val1 = value
    # value = int(hex(value), 16)

    # Get the most significant bits as row index
    x = value >> 4

    # Get the least significant bits as culomn index
    y = value & 15

    print(val1, value, x, y)
    return AES_sbox[0x10 * x + y]


def reverse_lookup(value):
    # Get the most significant bits as row index
    x = value >> 4

    # Get the least significant bits as culomn index
    y = value & 15

    return reverse_AES_sbox[x][y]


def shift_row(row):
    return row[1:] + row[:1]


def mix_columns(grid):
    new_grid = [[], [], [], []]
    for i in range(4):
        col = [grid[j][i] for j in range(4)]
        col = mix_column(col)
        for i in range(4):
            new_grid[i].append(col[i])
    return new_grid


def mix_column(column):
    r = [
        np.multiply(column[0], 0x2) ^ np.multiply(column[1], 0x3) ^ column[2] ^ column[3],
        np.multiply(column[1], 0x2) ^ np.multiply(column[2], 0x3) ^ column[3] ^ column[0],
        np.multiply(column[2], 0x2) ^ np.multiply(column[3], 0x3) ^ column[0] ^ column[1],
        np.multiply(column[3], 0x2) ^ np.multiply(column[0], 0x3) ^ column[1] ^ column[2],
    ]
    return r

def add_round_key(grid, key):
    output = []

    for i in range(4):
        output.append([])

        for j in range(4):
            print("xor:", grid[i][j], int(key[i][j], 16))
            output[-1].append(grid[i][j] ^ int(key[i][j], 16))

    return output
