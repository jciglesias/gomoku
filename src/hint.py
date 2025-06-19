import numpy as np

def alignements_column(board_size, win_len, tab, player, type = "row"):
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
                    if type == "row":
                        pieces.append((i, j))
                    else:
                        pieces.append((j, i))
                    k += 1
                    i += 1
                if k >= 3:
                    result.append(pieces)
            else:
                i += 1
        j += 1
    return result

def alignements_diag(board_size, win_len, tab, player, type = "diag"):
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
                    if type == "diag":
                        pieces.append((i, i - j))
                    else:
                        pieces.append((i - j, board_size - 1 - i))
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
    column = alignements_column(board_size, win_len, tab, player, "row")
    if column:
        res.append(column)
    row = alignements_column(board_size, win_len, tab.transpose(), player, "column")
    if row:
        res.append(row)
    diag = alignements_diag(board_size, win_len, tab, player, "diag")
    if diag:
        res.append(diag)
    diag_inv = alignements_diag(board_size, win_len, np.rot90(tab, k = 1), player, "diag_inv")
    if diag_inv:
        res.append(diag_inv)
    liste_aplatie = [item for sublist in res for inner_list in sublist for item in inner_list]
    ensemble_sans_doublons = list(set(liste_aplatie))
    return ensemble_sans_doublons
