import pandas as pd
import numpy as np
import time

def check_direction(board_size, win_len, tab, row, col, delta_row, delta_col):
    count = 0
    for k in range(win_len):
        r = row + k * delta_row
        c = col + k * delta_col
        if 0 <= r < board_size and 0 <= c < board_size and tab[r][c] == tab[row][col]:
            count += 1
        else:
            break
    return count == win_len

def heuristic(board_size, win_len, tab):
    start = time.perf_counter()
    for i in range(board_size):
        for j in range(board_size):
            if tab[i][j] is not np.nan:
                if check_direction(board_size, win_len, tab, i, j, 1, 0) or \
                    check_direction(board_size, win_len, tab, i, j, 0, 1) or \
                    check_direction(board_size, win_len, tab, i, j, 1, 1) or \
                    check_direction(board_size, win_len, tab, i, j, 1, -1):
                    return 100
    result = 0
    if win_len > 1:
        for i in range(board_size):
            for j in range(board_size):
                if tab[i][j] is not np.nan:
                    if check_direction(board_size, win_len - 1, tab, i, j, 1, 0) or \
                        check_direction(board_size, win_len - 1, tab, i, j, 0, 1) or \
                        check_direction(board_size, win_len - 1, tab, i, j, 1, 1) or \
                        check_direction(board_size, win_len - 1, tab, i, j, 1, -1):
                        result += 20
    if win_len > 2:
        for i in range(board_size):
            for j in range(board_size):
                if tab[i][j] is not np.nan:
                    if check_direction(board_size, win_len - 2, tab, i, j, 1, 0) or \
                        check_direction(board_size, win_len - 2, tab, i, j, 0, 1) or \
                        check_direction(board_size, win_len - 2, tab, i, j, 1, 1) or \
                        check_direction(board_size, win_len - 2, tab, i, j, 1, -1):
                        result += 10
    if win_len > 3:
        for i in range(board_size):
            for j in range(board_size):
                if tab[i][j] is not np.nan:
                    if check_direction(board_size, win_len - 3, tab, i, j, 1, 0) or \
                        check_direction(board_size, win_len - 3, tab, i, j, 0, 1) or \
                        check_direction(board_size, win_len - 3, tab, i, j, 1, 1) or \
                        check_direction(board_size, win_len - 3, tab, i, j, 1, -1):
                        result += 1
    end = time.perf_counter()
    print(f"Heuristic in {(end - start)*1000:0.4f} milliseconds")
    return result  