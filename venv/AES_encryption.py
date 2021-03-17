import numpy as np
from functions import *
from key_expansion import *

def encryption(data, key):
    
    pad = bytes(16 - len(data) % 16)
    data = data + pad if len(pad) != 16 else data

    grids = segmentation(data)

    # Expand the key
    expanded_key = keyExpansion(key)

    temp_grids = []
    round_key = expanded_key[:4]

    for grid in grids:
        temp_grids.append(add_round_key(grid, round_key))

    grids = temp_grids
    print("xxxxxxxxx:", grids)

    for round in range(1, 10):
        temp_grids = []

        for grid in grids:
            sub_bytes_step = [[lookup(val) for val in row] for row in grid]
            shift_rows_step = [shift_row(sub_bytes_step[i]) for i in range(4)]
            mix_column_step = mix_columns(shift_rows_step)
            round_key = expanded_key[4 * round : 4 * round + 4]
            add_round_key_step = add_round_key(mix_column_step, round_key)
            temp_grids.append(add_round_key_step)

        grids = temp_grids

    # Final round without the mix columns
    temp_grids = []
    round_key = expanded_key[-4:]

    for grid in grids:
        sub_bytes_step = [[lookup(val) for val in row] for row in grid]
        shift_rows_step = [shift_row(sub_bytes_step[i]) for i in range(4)]
        add_round_key_step = add_round_key(shift_rows_step, round_key)
        temp_grids.append(add_round_key_step)

    grids = temp_grids

    # Recriate the data into a single stream
    int_stream = []

    for grid in grids:
        for column in range(4):
            for row in range(4):
                int_stream.append(grid[row][column])

    return bytes(int_stream)
