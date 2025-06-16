import pandas as pd
import numpy as np
import time

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
                if tab[r][c] == 0:
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
        ('XXXXX', 100000),   # 5
        ('_XXXX', 10000),    # 4 opened
        ('XXXX_', 10000),    # 4 opened
        ('XXXX', 5000),      # 4 blocked
        ('_XXX', 1000),    # 3 opened
        ('XXX_', 1000),    # 3 opened
        ('XXX', 100),      # 3 blocked
        ('XX', 50),      # 3 blocked
        ('X', 10),      # 3 blocked
    ]
    for pattern, score in pattern_scores:
        index = 0
        while index < len(ligne):
            if ligne[index:].startswith(pattern):
                res += score
                index += 1
            else:
                index += 1
    return res

def heuristic(board_size, win_len, tab, player, row, col):
    lignes = getlines(board_size, 5, tab, player, row, col)
    res = 0
    for ligne in lignes:
        res += extract_motifs(ligne)
    return res