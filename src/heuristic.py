import pandas as pd
import numpy as np
from src.utils import check_alignement_capture, remove_captured
import functools

def heuristic_row(board_size, win_len, tab, player, reward):
    i = 0
    result = 0
    while i < board_size:
        j = 0
        while j <= board_size - 1:
            cell_value = tab[j][i]
            if cell_value == player:
                open = 0
                if j - 1 >= 0 and tab[j - 1][i] == 0:
                    open = 1
                k = 0
                while k < win_len and j < board_size and tab[j][i] == player:
                    k += 1
                    j += 1
                if j < board_size and tab[j][i] == 0:
                    open += 1
                result += reward[0][open][k]
            elif cell_value == -player:
                open = 0
                if j - 1 >= 0 and tab[j - 1][i] == 0:
                    open = 1
                k = 0
                lap = 0
                while k < win_len and j < board_size and tab[j][i] != player and lap < 2:
                    if tab[j][i] == -player:
                        k += 1
                        j += 1
                    else:
                        lap += 1
                        if j + 1 < board_size and tab[j + 1][i] == -player and lap == 1:
                            j += 1
                        else:
                            break
                if j < board_size and tab[j][i] == 0:
                    open += 1
                result += reward[1][open][k]
            else:
                j += 1
        i += 1
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
                    if i - 1 >= 0 and i - 1 - j >= 0 and tab[i - 1][i - 1 - j] == 0:
                        open = 1
                    k = 0
                    while k < win_len and i < min_board and tab[i][i - j] == player:
                        k += 1
                        i += 1
                    if i < board_size and i - j < board_size and cell_value == 0:
                            open += 1
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
        res -= reward_capture[1][g_score[-player]]
    return res

def get_oponent(val, a, b, win_len):
    if val == 10**(2 * win_len - 5):
        return -val
    return -val * a + b

@functools.lru_cache
def get_reward(win_len):
    reward_closed = [0] * (win_len + 1)
    reward_open1 = [0] + [10**i for i in range(-4, 2 * win_len - 4, 2)]
    reward_open2 = [0] + [10**i for i in range(-3, 2 * win_len - 3, 2)]
    reward_closed[win_len] = 10**(2 * win_len - 5)
    reward_open1[win_len] = 10**(2 * win_len - 5)
    reward = [reward_closed, reward_open1, reward_open2]
    reward_block = [[get_oponent(val, 1.5, 0, win_len) for val in lst] for lst in reward]
    reward = [np.array(reward), np.array(reward_block)]
    reward_capture = [10 + (i + 1) for i in range(5)]
    reward_capture[4] = 10**(2 * win_len - 5)
    reward_capture_block = [ get_oponent(val, 1, 10, win_len)  for val in reward_capture]
    reward_capture = [np.array(reward_capture), np.array(reward_capture_block)]
    return reward, reward_capture

def heuristic(board_size, win_len, tab, player, row, col, g_score, game_rules=["Capture", "Double Three"]):
    reward, reward_capture = get_reward(win_len)
    tab = np.array(tab)
    res = 0
    if 'Capture' in game_rules:
        res += heuristic_capture(tab, player, row, col, g_score, reward_capture)
        if res != 0:
            tab, _ = remove_captured(tab, row, col, 0, player)
    res += heuristic_row(board_size, win_len, tab, player, reward)
    res += heuristic_row(board_size, win_len, tab.transpose(), player, reward)
    res += heuristic_diag(board_size, win_len, tab, player, reward)
    res += heuristic_diag(board_size, win_len, np.rot90(tab, k = 1), player, reward)
    return res

def heuristic_score(win_len):
    df, dt = get_reward(win_len)
    df_1 = pd.DataFrame(df[0])
    df_1.index = ['Score for closed', 'Score for semi-opened', 'Score for opened']
    df_2 = pd.DataFrame(df[1])
    df_2.index = ['Score for closed', 'Score for semi-opened', 'Score for opened']
    dt_1 = pd.DataFrame(dt[0]).T
    dt_1.index = ['Score']
    dt_2 = pd.DataFrame(dt[1]).T
    dt_2.index = ['Score']
    return [df_1, df_2], [dt_1, dt_2]