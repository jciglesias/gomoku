import numpy as np

directions = [(-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
            ]

def check_column(board_size, win_len, tab, player):
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
                        while k < win_len and j < board_size and tab[j][i] != -player and lap < 2:
                            if tab[j][i] == player:
                                k += 1
                            else:
                                lap += 1
                            j += 1
                        if j < board_size:
                            if tab[j][i] == 0 and k == 3:
                                result += 1
                    else:
                        j += 1
                else:
                    j += 1
            else:
                j += 1
        i += 1
    return result

def check_diag(board_size, win_len, tab, player):
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
                            while k < win_len and i < min(board_size, j + board_size) and tab[i][i - j] != -player and lap < 2:
                                if tab[i][i - j] == player:
                                    k += 1
                                else:
                                    lap += 1
                                i += 1
                            if i < board_size and i - j < board_size:
                                if tab[i][i - j] == 0 and k == 3:
                                    result += 1
                    else:
                        i += 1
                else:
                    i += 1
            else:
                i += 1
        j += 1
    return result

def check_threes(board, row, col, empty_cell, player):
    tab = np.array(board)
    tab[row][col] = player
    res = check_column(len(board), 3, tab, player)
    res += check_column(len(board), 3, tab.transpose(), player)
    res += check_diag(len(board), 3, tab, player)
    res += check_diag(len(board), 3, np.rot90(tab, k = 1), player)
    return (res >= 2)

def check_capture(board, row, col, empty_cell, player):
    # Check if the move captures exactly two opponent pieces
    if board[row][col] != empty_cell:
        return False
    # Check all 8 directions for a capture
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < len(board) and 0 <= c < len(board):
            if board[r][c] == -player:  # Found an opponent piece
                # search in the same direction for another opponent piece
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < len(board) and 0 <= c2 < len(board):
                    if board[r2][c2] == -player:
                        # check if the next cell in the same direction is player's piece
                        r3, c3 = r2 + dr, c2 + dc
                        if 0 <= r3 < len(board) and 0 <= c3 < len(board):
                            if board[r3][c3] == player:
                                return True
    return False

def check_valid_move(board, row, col, empty_cell, player):
    if board[row][col] != empty_cell:
        return False
    # check if the move creates a double-three
    # if check_threes(board, row, col, empty_cell, player):
    #     return False
    return True