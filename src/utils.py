from copy import deepcopy
marks = {
    0: ':material/radio_button_unchecked:',
    1: ':red[:material/cancel:]',
    -1: ':green[:material/check_circle:]'
}

def make_move(board_og, row, col, player, empty_cell) -> list:
    board = deepcopy(board_og)
    if board[row][col] == empty_cell:
        board[row][col] = player
    return board

def check_winner(board, empty_cell, board_size, win_len):
    for i in range(board_size):
        for j in range(board_size):
            if board[i][j] != empty_cell:
                if check_direction(i, j, 1, 0, board_size, win_len, board) or check_direction(i, j, 0, 1, board_size, win_len, board) or \
                   check_direction(i, j, 1, 1, board_size, win_len, board) or check_direction(i, j, 1, -1, board_size, win_len, board):
                    return 1
    if all(board[i][j] != empty_cell for i in range(board_size) for j in range(board_size)):
        return -1
    return 0

def check_direction(row, col, delta_row, delta_col, board_size, win_len, board):
    count = 0
    for k in range(win_len):
        r = row + k * delta_row
        c = col + k * delta_col
        if 0 <= r < board_size and 0 <= c < board_size and board[r][c] == board[row][col]:
            count += 1
        else:
            break
    return count == win_len

def reset_game(empty_cell, board_size):
    return [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    
def switch_player(player):
    return player * -1

def check_threes(board, row, col, empty_cell, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]
    threes = 0
    for dr, dc in directions:
        count = 0
        for k in range(-2, 3):  # Check both sides of the current cell
            r = row + k * dr
            c = col + k * dc
            if 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] == player:
                count += 1
            elif 0 <= r < len(board) and 0 <= c < len(board) and board[r][c] != empty_cell:
                count = 0
            if count >= 3:
                threes += 1
    return threes >= 2

def check_valid_move(board, row, col, empty_cell, player):
    if board[row][col] != empty_cell:
        return False
    # check if the move creates a double-three
    if check_threes(board, row, col, empty_cell, player):
        return False
    return True

