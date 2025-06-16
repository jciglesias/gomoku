import pandas as pd
import numpy as np
import time

directions = [(-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
            ]

def heuristic(board_size, win_len, tab, player, row, col):
    res = 0
    for i in range(8):
        r = row  + directions[i][0]
        c = col + directions[i][1]
        if 0 <= r < board_size and 0 <= c < board_size:
            if tab[r][c] == -player: # check capture
                r = row - directions[i][0]
                c = col - directions[i][1]
                if 0 <= r < board_size and 0 <= c < board_size:
                    if tab[r][c] == -player:
                        r = row  - directions[i][0] * 2
                        c = col - directions[i][1] * 2
                        if 0 <= r < board_size and 0 <= c < board_size:
                            if tab[r][c] == player:
                                res += 10 # reward capture
    return res