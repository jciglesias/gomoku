import pandas as pd
import numpy as np
import re

directions = [(0, 1),
            (1, 0),
            (1, 1),
            (-1, 1)
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
    pattern_scores = [
        ('XOOx',   10000),   # capture
        ('xOOX',   10000),   # capture

        ('xXXXX',  10000000),   # 5
        ('XxXXX',  10000000),   # 5
        ('XXXxX',  10000000),   # 5
        ('XXXXx',  10000000),   # 5

        ('_xXXX_', 1000000),   # 4 opened
        ('_XxXX_', 1000000),   # 4 opened
        ('_XXxX_', 1000000),   # 4 opened
        ('_XXXx_', 1000000),   # 4 opened

        ('YxXXX_', 100000),   # 4 blocked
        ('YXxXX_', 100000),   # 4 blocked
        ('YXXxX_', 100000),   # 4 blocked
        ('YXXXx_', 100000),   # 4 blocked

        ('_xXXXY', 100000),   # 4 blocked
        ('_XxXXY', 100000),   # 4 blocked
        ('_XXxXY', 100000),   # 4 blocked
        ('_XXXxY', 100000),   # 4 blocked

        ('_xXX_',  10000),   # 3 opened
        ('_XxX_',  10000),   # 3 opened
        ('_XXx_',  10000),   # 3 opened

        ('YxXX_',  1000),   # 3 blocked
        ('YXxX_',  1000),   # 3 blocked
        ('YXXx_',  1000),   # 3 blocked

        ('_xXXY',  1000),   # 3 blocked
        ('_XxXY',  1000),   # 3 blocked
        ('_XXxY',  1000),   # 3 blocked

        ('_Xx_',   100),   # 2 opened
        ('_Xx_',   100),   # 2 opened

        ('YXx_',   10),   # 2 blocked
        ('YXx_',   10),   # 2 blocked

        ('_XxY_',  10),   # 2 blocked
        ('_XxY',   10),   # 2 blocked

        ('_x_',   11),   # 1 opened

        ('xYYYY', 1100000),   # block a 4
        ('YYYYx', 1100000),   # block a 4

        ('xYYY',  11000),   # block a 3
        ('YYYx',  11000),   # block a 3

        ('xYYY',  110),   # block a 2
        ('YYYx',  110),   # block a 2
    ]
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