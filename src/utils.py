from copy import deepcopy
marks = {
    0: ':material/radio_button_unchecked:',
    -1: ':material/cancel:',
    1: ':material/check_circle:'
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