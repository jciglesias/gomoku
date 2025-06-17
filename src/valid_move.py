import numpy as np

def check_column(board_size, win_len, tab, player, row, col):
    i = 0
    result = 0
    while i < board_size:
        j = 0
        while j <= board_size - 1:
            if tab[j][i] == player:
                if j - 1 >= 0:
                    if tab[j - 1][i] == 0:
                        k = 0
                        lap = 0
                        valid = 0
                        while k < win_len and j < board_size and tab[j][i] != -player and lap < 2:
                            if i == row and j == col:
                                valid = 1
                            if tab[j][i] == player:
                                k += 1
                            else:
                                lap += 1
                            j += 1
                        if j < board_size:
                            if tab[j][i] == 0 and k == 3 and valid == 1:
                                result += 1
                    else:
                        j += 1
                else:
                    j += 1
            else:
                j += 1
        i += 1
    return result

def check_diag(board_size, win_len, tab, player, row, col):
    result = 0
    j =  1 - board_size
    while j < board_size:
        i = max(0, j)
        while i < min(board_size, j + board_size):
            if tab[i][i - j] == player:
                if i - 1 >= 0 and i - 1 - j >= 0:
                    if tab[i - 1][i - 1 - j] == 0:
                            k = 0
                            lap = 0
                            valid = 0
                            while k < win_len and i < min(board_size, j + board_size) and tab[i][i - j] != -player and lap < 2:
                                if i == row and i - j == col:
                                    valid = 1
                                if tab[i][i - j] == player:
                                    k += 1
                                else:
                                    lap += 1
                                i += 1
                            if i < board_size and i - j < board_size:
                                if tab[i][i - j] == 0 and k == 3 and valid == 1:
                                    result += 1
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        j += 1
    return result

def check_threes(board, player, row, col):
    tab = np.array(board)
    tab[row][col] = player
    res = check_column(len(board), 3, tab, player, col, row)
    res += check_column(len(board), 3, tab.transpose(), player, row, col)
    res += check_diag(len(board), 3, tab, player, row, col)
    res += check_diag(len(board), 3, np.rot90(tab, k = 1), player, len(board) - 1 - col, row)
    return (res >= 2)

def check_valid_move(board, row, col, empty_cell, player,  game_rules):
    if board[row][col] != empty_cell:
        return False
    # check if the move creates a double-three
    if 'Double Three' in game_rules and check_threes(board, player, row, col):
        return False
    return True