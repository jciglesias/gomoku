import numpy as np

def alignements_column(board_size, win_len, tab, player):
    j = 0
    result = []
    while j < board_size:
        i = 0
        while i <= board_size - 1:
            cell_value = tab[i][j]
            if cell_value == player:
                k = 0
                pieces =  []
                while k < win_len and i < board_size and tab[i][j] == player:
                    k += 1
                    i += 1
                    pieces.append((i, j))
                if k > 3:
                    result.append(pieces)
            else:
                i += 1
        j += 1
    return 1

def alignements_diag(board_size, win_len, tab, player):
    return 1



def check_alignements(board_size, win_len, tab, player):
    align = []
    tab = np.array(tab)
    res = alignements_column(board_size, win_len, tab, player)
    res = alignements_column(board_size, win_len, tab.transpose())
    res = alignements_diag(board_size, win_len, tab, player)
    res = alignements_diag(board_size, win_len, np.rot90(tab, k = 1), player)
    return res

    return align
