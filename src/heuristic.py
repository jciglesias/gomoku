import pandas as pd
import numpy as np
import time
from src.utils import check_alignement_capture

def check_direction(board_size, win_len, tab, player, row, col, delta_row, delta_col):
    count = 0
    for k in range(win_len):
        r = row + k * delta_row
        c = col + k * delta_col
        if 0 <= r < board_size and 0 <= c < board_size and tab[r][c] == tab[row][col] and tab[r][c] == player:
            count += 1
        else:
            break
    return count == win_len

def heuristic_row(board_size, win_len, tab, player, reward):
    i = 0
    result = 0
    while i < board_size:
        j = 0
        while j <= board_size - 1:
            if tab[j][i] == player:
                open = 0
                if j - 1 >= 0:
                    if tab[j - 1][i] == 0:
                        open = 1
                k = 0
                while k < win_len and j < board_size and tab[j][i] == player:
                    k += 1
                    j += 1
                if j < board_size:
                    if tab[j][i] == 0:
                        open += 1
                result += reward[open][k]
            elif tab[j][i] == -player:
                open = 0
                if j - 1 >= 0:
                    if tab[j - 1][i] == 0:
                        open = 1
                k = 0
                while k < win_len and j < board_size and tab[j][i] == -player:
                    k += 1
                    j += 1
                if j < board_size:
                    if tab[j][i] == 0:
                        open += 1
                result -= reward[open][k]
            else:
                j += 1
        i += 1
    return result

def heuristic_diag(board_size, win_len, tab, player, reward):
    result = 0
    j =  1 - board_size
    while j < board_size:
        i = max(0, j)
        while i < min(board_size, j + board_size):
            if tab[i][i - j] == player:
                    open = 0
                    if i - 1 >= 0 and i - 1 - j >= 0:
                        if tab[i - 1][i - 1 - j] == 0:
                            open = 1
                    k = 0
                    while k < win_len and i < min(board_size, j + board_size) and tab[i][i - j] == player:
                        k += 1
                        i += 1
                    if i < board_size and i - j < board_size:
                        if tab[i][i - j] == 0:
                            open += 1
                    result += reward[open][k]
            elif tab[i][i - j] == -player:
                    open = 0
                    if i - 1 >= 0 and i - 1 - j >= 0:
                        if tab[i - 1][i - 1 - j] == 0:
                            open = 1
                    k = 0
                    while k < win_len and i < min(board_size, j + board_size) and tab[i][i - j] == -player:
                        k += 1
                        i += 1
                    if i < board_size and i - j < board_size:
                        if tab[i][i - j] == 0:
                            open += 1
                    result -= reward[open][k] * 1.5
            else:
                i += 1
        j += 1
    return result

def heuristic_capture(tab, player, row, col, g_score, reward_capture):
    res = 0
    if check_alignement_capture(tab, row, col, player):
        res += reward_capture[g_score[player]]
    if check_alignement_capture(tab, row, col, -player):
        res -= reward_capture[g_score[-player]] + 200
    return res

def heuristic(board_size, win_len, tab, player, row, col, g_score):
    reward_closed = [0] * (win_len + 1)
    reward_open1 = [0] + [0] + [10**i for i in range(-2, win_len, 2)]
    reward_open2 = [0] + [0] + [10**i for i in range(-1, win_len + 1, 2)]
    reward_closed[win_len] = 10**(win_len)
    reward_open1[win_len] = 10**(win_len)
    reward = [reward_closed, reward_open1, reward_open2]
    reward_capture = [100 + 10**(i+1) for i in range(5)]
    reward_capture[4] = 10**(win_len)
    tab = np.array(tab)
    res = heuristic_capture(tab, player, row, col, g_score, reward_capture)
    res += heuristic_row(board_size, win_len, tab, player, reward)
    res += heuristic_row(board_size, win_len, tab.transpose(), player, reward)
    res += heuristic_diag(board_size, win_len, tab, player, reward)
    res += heuristic_diag(board_size, win_len, np.rot90(tab, k = 1), player, reward)
    return res