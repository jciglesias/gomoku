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
                    ligne += 'Y'
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
        ('XOOY', 100000),   # capture
        ('YOOX', 100000)    # capture
    ]
    for pattern, score in pattern_scores:
        match = re.search(pattern, ligne)
        print(f"Pattern {pattern} ligne {ligne} match {match}")
        if match:
            res += score
    return res

def heuristic(board_size, win_len, tab, player, row, col):
    lignes = getlines(board_size, 5, tab, player, row, col)
    res = 0
    for ligne in lignes:
        res += extract_motifs(ligne)
    return res