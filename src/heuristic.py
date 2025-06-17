import pandas as pd
import numpy as np
import re

directions = [(0, 1),
            (1, 0),
            (1, 1),
            (-1, 1)
            ]

pattern_scores = [
    ('XOOx',   10000),   # capture
    ('xOOX',   10000),   # capture

    ('xXXXX',  10000000),   # 5
    ('XxXXX',  10000000),   # 5
    ('XXXxX',  10000000),   # 5
    ('XXXXx',  10000000),   # 5

    ('_x_XXX_', 1000000),   # 4 opened
    ('_X_xXX_', 1000000),   # 4 opened
    ('_X_XxX_', 1000000),   # 4 opened
    ('_X_XXx_', 1000000),   # 4 opened

    ('_x_XXX_', 1000000),   # 4 opened
    ('_X_xXX_', 1000000),   # 4 opened
    ('_X_XxX_', 1000000),   # 4 opened
    ('_X_XXx_', 1000000),   # 4 opened

    ('_xX_XX_', 1000000),   # 4 opened
    ('_Xx_XX_', 1000000),   # 4 opened
    ('_XX_xX_', 1000000),   # 4 opened
    ('_XX_Xx_', 1000000),   # 4 opened

    ('_xXX_X_', 1000000),   # 4 opened
    ('_XxX_X_', 1000000),   # 4 opened
    ('_XXx_X_', 1000000),   # 4 opened
    ('_XXX_x_', 1000000),   # 4 opened

    ('YxXXX_', 100000),   # 4 blocked
    ('YXxXX_', 100000),   # 4 blocked
    ('YXXxX_', 100000),   # 4 blocked
    ('YXXXx_', 100000),   # 4 blocked

    ('Yx_XXX_', 90000),   # 4 blocked with gap
    ('YX_xXX_', 90000),   # 4 blocked with gap
    ('YX_XxX_', 90000),   # 4 blocked with gap
    ('YX_XXx_', 90000),   # 4 blocked with gap

    ('YxX_XX_', 90000),   # 4 blocked with gap
    ('YXx_XX_', 90000),   # 4 blocked with gap
    ('YXX_xX_', 90000),   # 4 blocked with gap
    ('YXX_Xx_', 90000),   # 4 blocked with gap

    ('YxXX_X_', 90000),   # 4 blocked with gap
    ('YXxX_X_', 90000),   # 4 blocked with gap
    ('YXXx_X_', 90000),   # 4 blocked with gap
    ('YXXX_x_', 90000),   # 4 blocked with gap

    ('_xXXXY', 100000),   # 4 blocked
    ('_XxXXY', 100000),   # 4 blocked
    ('_XXxXY', 100000),   # 4 blocked
    ('_XXXxY', 100000),   # 4 blocked

    ('_x_XXXY', 90000),   # 4 blocked with gap
    ('_X_xXXY', 90000),   # 4 blocked with gap
    ('_X_XxXY', 90000),   # 4 blocked with gap
    ('_X_XXxY', 90000),   # 4 blocked with gap

    ('_xX_XXY', 90000),   # 4 blocked with gap
    ('_Xx_XXY', 90000),   # 4 blocked with gap
    ('_XX_xXY', 90000),   # 4 blocked with gap
    ('_XX_XxY', 90000),   # 4 blocked with gap

    ('_xXX_XY', 90000),   # 4 blocked with gap
    ('_XxX_XY', 90000),   # 4 blocked with gap
    ('_XXx_XY', 90000),   # 4 blocked with gap
    ('_XXX_xY', 90000),   # 4 blocked with gap

    ('_xXX_',  10000),   # 3 opened
    ('_XxX_',  10000),   # 3 opened
    ('_XXx_',  10000),   # 3 opened

    ('_x_XX_',  9000),   # 3 opened with gap
    ('_X_xX_',  9000),   # 3 opened with gap
    ('_X_Xx_',  9000),   # 3 opened with gap
    ('_xX_X_',  9000),   # 3 opened with gap
    ('_Xx_X_',  9000),   # 3 opened with gap
    ('_XX_x_',  9000),   # 3 opened with gap

    ('YxXX_',  1000),   # 3 blocked
    ('YXxX_',  1000),   # 3 blocked
    ('YXXx_',  1000),   # 3 blocked

    ('Yx_XX_',  900),   # 3 blocked with gap
    ('YX_xX_',  900),   # 3 blocked with gap
    ('YX_Xx_',  900),   # 3 blocked with gap
    ('YxX_X_',  900),   # 3 blocked with gap
    ('YXx_X_',  900),   # 3 blocked with gap
    ('YXX_x_',  900),   # 3 blocked with gap

    ('_xXXY',  1000),   # 3 blocked
    ('_XxXY',  1000),   # 3 blocked
    ('_XXxY',  1000),   # 3 blocked

    ('_x_XXY',  900),   # 3 blocked with gap
    ('_X_xXY',  900),   # 3 blocked with gap
    ('_X_XxY',  900),   # 3 blocked with gap
    ('_xX_XY',  900),   # 3 blocked with gap
    ('_Xx_XY',  900),   # 3 blocked with gap
    ('_XX_xY',  900),   # 3 blocked with gap

    ('_Xx_',   100),   # 2 opened
    ('_Xx_',   100),   # 2 opened

    ('_X_x_',   90),   # 2 opened with gap
    ('_X_x_',   90),   # 2 opened with gap

    ('YXx_',   10),    # 2 blocked
    ('YxX_',   10),    # 2 blocked

    ('YX_x_',   10),   # 2 blocked with gap
    ('Yx_X_',   10),   # 2 blocked with gap

    ('_XxY',  10),     # 2 blocked
    ('_xXY',   10),    # 2 blocked

    ('_X_xY',  10),     # 2 blocked with gap
    ('_x_XY',   10),    # 2 blocked with gap

    ('_x_',   11),     # 1 opened

    ('xYYYYY',  11000000),  # block a 5
    ('YxYYYY',  11000000),  # block a 5
    ('YYxYYY',  11000000),  # block a 5
    ('YYYxYY',  11000000),  # block a 5
    ('YYYYxY',  11000000),  # block a 5
    ('YYYYYx',  11000000),  # block a 5

    ('xYYYY', 1100000),   # block a 4
    ('YxYYY', 1100000),   # block a 4
    ('YYxYY', 1100000),   # block a 4
    ('YYYxY', 1100000),   # block a 4
    ('YYYYx', 1100000),   # block a 4

    ('xYYY',  11000),   # block a 3
    ('YxYY',  11000),   # block a 3
    ('YYxY',  11000),   # block a 3
    ('YYYx',  11000),   # block a 3

    ('xYY',  110),   # block a 2
    ('YxY',  110),   # block a 2
    ('YYx',  110),   # block a 2

    ('_xXY',  10000),   # avoid capture
    ('_XxY',  10000),   # avoid capture
    ('YXx_',  10000),   # avoid capture
    ('YXx_',  10000),   # avoid capture

]

def getlines(board_size, win_len, tab, player, row, col):
    lignes = []
    for i in range(win_len - 1):
        ligne = ''  
        for j in range(-(win_len - 1), win_len):
            r = row + j * directions[i][0]
            c = col + j * directions[i][1]
            if 0 <= r < board_size and 0 <= c < board_size:
                if r == row and c == col:
                    ligne += 'x'
                elif tab[r][c] == 0:
                    ligne += '_'
                elif tab[r][c] == player:
                    ligne += 'X'
                else:
                    ligne += 'O'
        lignes.append(ligne)
    return lignes

def extract_motifs(ligne):
    res = 0
    for pattern, score in pattern_scores:
        match = re.search(pattern, ligne)
        #print(f"Pattern {pattern} ligne {ligne} match {match}")
        if match:
            res += score
    return res

def heuristic(board_size, win_len, tab, player, row, col):
    lignes = getlines(board_size, 5, tab, player, row, col)
    res = 0
    for ligne in lignes:
        res += extract_motifs(ligne)
    return res