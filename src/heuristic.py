import pandas as pd
import numpy as np
from src.utils import check_alignement_capture, remove_captured
import functools

def heuristic_column(board_size, win_len, tab, player, reward):
    j = 0
    result = 0
    while j < board_size:
        i = 0
        while i <= board_size - 1:
            cell_value = tab[i][j]
            if cell_value == player:
                open = 0
                if i > 0 and tab[i - 1][j] == 0:
                    open = 1
                k = 0
                while k < win_len and i < board_size and tab[i][j] == player:
                    k += 1
                    i += 1
                if i < board_size and tab[i][j] == 0:
                    open += 1
                    if k == 3 and open == 1 and (i + 1 >= board_size or (i + 1 < board_size and tab[i + 1][j] == -player)):
                        open = 0
                elif k == 3 and open == 1 and (i - k  - 2 < 0  or (i - k  - 2 >= 0 and tab[i - k  - 2][j] == -player)):
                    open = 0
                result += reward[0][open][k]
            elif cell_value == -player:
                open = 0
                if i - 1 >= 0 and tab[i - 1][j] == 0:
                    open = 1
                k = 0
                lap = 0
                while k < win_len and i < board_size and tab[i][j] != player and lap < 2:
                    if tab[i][j] == -player:
                        k += 1
                        i += 1
                    else:
                        lap += 1
                        if i + 1 < board_size and tab[i + 1][j] == -player and lap == 1:
                            i += 1
                        else:
                            break
                if i < board_size and tab[i][j] == 0:
                    open += 1
                    if k == 3 and open == 1 and (i + 1 >= board_size or (i + 1 < board_size and tab[i + 1][j] == player)):
                        open = 0
                elif k == 3 and open == 1 and (i - k  - 2 < 0  or (i - k  - 2 >= 0 and tab[i - k  - 2][j] == player)):
                    open = 0
                result += reward[1][open][k]
            else:
                i += 1
        j += 1
    return result

def heuristic_diag(board_size, win_len, tab, player, reward):
    result = 0
    j =  1 - board_size
    while j < board_size:
        i = max(0, j)
        min_board = min(board_size, j + board_size)
        while i < min_board:
            cell_value = tab[i][i - j]
            if cell_value == player:
                    open = 0
                    if i > 0 and i - j > 0 and tab[i - 1][i - 1 - j] == 0:
                        open = 1
                    k = 0
                    while k < win_len and i < min_board and tab[i][i - j] == player:
                        k += 1
                        i += 1
                    if i < board_size and i - j < board_size and tab[i][i - j] == 0:
                        open += 1
                        if k == 3 and open == 1 and ((i + 1 >= board_size or i + 1 - j >= board_size) or (i + 1 < board_size and i + 1 - j < board_size and tab[i + 1][i + 1 - j] == -player)):
                            open = 0
                    elif k == 3 and open == 1 and ((i - k - 2 < 0 or i - k - 2 - j < 0) or (i - k - 2 >= 0 and i - k - 2 - j >= 0 and tab[i - k - 2][i - k - 2 - j] == -player)):
                        open = 0
                    result += reward[0][open][k]
            elif cell_value == -player:
                    open = 0
                    if i > 0 and i - j > 0 and tab[i - 1][i - 1 - j] == 0:
                        open = 1
                    k = 0
                    lap = 0
                    while k < win_len and i < min_board and tab[i][i - j] != player and lap < 2:
                        if tab[i][i - j] == -player:
                            k += 1
                            i += 1
                        else:
                            lap += 1
                            if i + 1 < min_board and tab[i + 1][i + 1 - j] == -player and lap == 1:
                                i += 1
                            else:
                                break
                    if i < board_size and i - j < board_size and tab[i][i - j] == 0:
                        open += 1
                        if k == 3 and open == 1 and ((i + 1 >= board_size or i + 1 - j >= board_size) or (i + 1 < board_size and i + 1 - j < board_size and tab[i + 1][i + 1 - j] == player)):
                            open = 0
                    elif k == 3 and open == 1 and ((i - k - 2 < 0 or i - k - 2 - j < 0) or (i - k - 2 >= 0 and i - k - 2 - j >= 0 and tab[i - k - 2][i - k - 2 - j] == player)):
                        open = 0
                    result += reward[1][open][k]
            else:
                i += 1
        j += 1
    return result

def heuristic_capture(tab, player, row, col, g_score, reward_capture):
    res = 0
    if check_alignement_capture(tab, row, col, player):
        res += reward_capture[0][g_score[player]]
    if check_alignement_capture(tab, row, col, -player):
        res += reward_capture[1][g_score[-player]]
    return res

def get_oponent(val, a, b, win_len):
    if val == 10**(2 * win_len - 5):
        return  -val
    return val * a + b

@functools.lru_cache
def get_reward(win_len, player=1, moy_block=0.5):
    reward_closed = [0] * (win_len + 1)
    reward_open1 = [0] + [10**i for i in range(-4, 2 * win_len - 4, 2)]
    reward_open2 = [0] + [10**i for i in range(-3, 2 * win_len - 3, 2)]
    reward_closed[win_len] = 10**(2 * win_len - 5)
    reward_open1[win_len] = 10**(2 * win_len - 5)
    reward = [reward_closed, reward_open1, reward_open2]
    if player == 1: #bot
        coeff = - 1 - (1 - moy_block) / 2
    else: #player
        coeff = -1.5
    reward_block = [[get_oponent(val, coeff, 0, win_len) for val in lst] for lst in reward]
    reward = [np.array(reward), np.array(reward_block)]
    reward_capture = [10 + (i + 1) for i in range(5)]
    reward_capture[4] = 10**(2 * win_len - 5)
    reward_capture_block = [ get_oponent(val, -1, 10, win_len)  for val in reward_capture]
    reward_capture = [np.array(reward_capture), np.array(reward_capture_block)]
    return reward, reward_capture

def heuristic(board_size, win_len, tab, player, row, col, g_score, game_rules=["Capture", "Double Three"]):
    reward, reward_capture = get_reward(win_len, player, g_score[-2])
    tab = np.array(tab)
    res = 0
    if 'Capture' in game_rules:
        res += heuristic_capture(tab, player, row, col, g_score, reward_capture)
        if res != 0:
            tab, _ = remove_captured(tab, row, col, 0, player)
    res1 = heuristic_column(board_size, win_len, tab, player, reward)
    res2 = heuristic_column(board_size, win_len, tab.transpose(), player, reward)
    res3 = heuristic_diag(board_size, win_len, tab, player, reward)
    res4 = heuristic_diag(board_size, win_len, np.rot90(tab, k = 1), player, reward)
    combinaison = sum(x > 10 for x in [res1, res2, res3, res4])
    if combinaison >= 2:
        return res + res1 + res2 + res3 + res4 + 10
    return res + res1 + res2 + res3 + res4

def heuristic_score(win_len, moy_block):
    df, dt = get_reward(win_len, player=1, moy_block=moy_block)
    df_1 = pd.DataFrame(df[0]).iloc[:, 1:]
    df_1.index = ['Score for closed', 'Score for semi-opened', 'Score for opened']
    df_2 = pd.DataFrame(df[1]).iloc[:, 1:]
    df_2.index = ['Score for closed', 'Score for semi-opened', 'Score for opened']
    dt_1 = pd.DataFrame(dt[0]).T
    dt_1.index = ['Score']
    dt_1.columns = ['1', '2', '3', '4', '5']
    dt_2 = pd.DataFrame(dt[1]).T
    dt_2.index = ['Score']
    dt_2.columns = ['1', '2', '3', '4', '5']
    return [df_1, df_2], [dt_1, dt_2]
