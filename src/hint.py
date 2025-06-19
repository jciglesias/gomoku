import numpy as np

def alignements_column(board_size, win_len, tab, player):
    j = 0
    result = []
    while j < board_size:
        i = 0
        while i < board_size:
            cell_value = tab[i][j]
            if cell_value == player:
                k = 0
                pieces = []
                while k < win_len and i < board_size and tab[i][j] == player:
                    pieces.append((i, j))
                    k += 1
                    i += 1
                if k >= 3:
                    result.append(pieces)
            else:
                i += 1
        j += 1
    return 1

def alignements_diag(board_size, win_len, tab, player):
    result = []
    j =  1 - board_size
    while j < board_size:
        i = max(0, j)
        min_board = min(board_size, j + board_size)
        while i < min_board:
            cell_value = tab[i][i - j]
            if cell_value == player:
                pieces = []
                k = 0
                while k < win_len and i < min_board and tab[i][i - j] == player:
                    pieces.append((i, j))
                    k += 1
                    i += 1
                if k >= 3:
                    result.append(pieces)
            else:
                i += 1
        j += 1
    return result

def check_alignements(board_size, win_len, tab, player):
    res = []
    tab = np.array(tab)
    res.append(alignements_column(board_size, win_len, tab, player))
    print(res)
    res.append(alignements_column(board_size, win_len, tab.transpose(), player))
    print(res)
    res.append(alignements_diag(board_size, win_len, tab, player))
    print(res)
    res.append(alignements_diag(board_size, win_len, np.rot90(tab, k = 1), player))
    print(res)
    return res
