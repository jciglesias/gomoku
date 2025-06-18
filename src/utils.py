from copy import deepcopy

marks = {
    0: ':material/radio_button_unchecked:',
    1: ':red[:material/cancel:]',
    -1: ':green[:material/check_circle:]'
}

def check_alignement_capture(board, row, col, player):
    board_size = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < board_size and 0 <= c < board_size:
            if board[r][c] == -player:  # Found an opponent piece
                # search in the same direction for another opponent piece
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < board_size and 0 <= c2 < board_size:
                    if board[r2][c2] == -player:
                        # check if the next cell in the same direction is player's piece
                        r3, c3 = r2 + dr, c2 + dc
                        if 0 <= r3 < board_size and 0 <= c3 < board_size:
                            if board[r3][c3] == player:
                                return True
    return False

def check_capture(board, row, col, empty_cell, player):
    # Check if the move captures exactly two opponent pieces
    if board[row][col] != empty_cell:
        return False
    # Check all 8 directions for a capture
    return check_alignement_capture(board, row, col, player)

def remove_captured(board, row, col, empty_cell, player):
    board_size = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count_captured = 0
    # Check all 8 directions for a capture
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < board_size and 0 <= c < board_size:
            if board[r][c] == -player:  # Found an opponent piece
                # search in the same direction for another opponent piece
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < board_size and 0 <= c2 < board_size:
                    if board[r2][c2] == -player:
                        # check if the next cell in the same direction is player's piece
                        r3, c3 = r2 + dr, c2 + dc
                        if 0 <= r3 < board_size and 0 <= c3 < board_size:
                            if board[r3][c3] == player:
                                count_captured += 1
                                # Remove the captured pieces
                                board[r][c] = empty_cell
                                board[r2][c2] = empty_cell
    return board, count_captured

def make_move(board_og, row, col, player, empty_cell, score=None, game_rules=[]) -> list:
    board = deepcopy(board_og)
    is_capture = check_capture(board, row, col, empty_cell, player)
    # print(f"Check {row,col}",is_capture)
    if board[row][col] == empty_cell:
        board[row][col] = player
        if is_capture and 'Capture' in game_rules:
            # print(f"Capture at {row,col}")
            board, n_captures = remove_captured(board, row, col, empty_cell, player)
            if score is not None:
                score[player] +=  n_captures
    del board_og
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

def reset_game(empty_cell, board_size, type_start):
    if type_start not in ['Pro', 'Long Pro']:
        return [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    else:
        # start with -1 in the center for Pro and Long Pro
        center = board_size // 2
        board = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
        board[center][center] = -1
        return board
    
def switch_player(player):
    return player * -1

def get_button_type(last_move, i, j, suggestion=None):
    if suggestion and (i, j) in suggestion:
        return "primary"
    if last_move and last_move == (i, j):
        return "secondary"
    return "tertiary"

def check_empty_board(board, empty_cell):
    return all(cell == empty_cell for row in board for cell in row)

def debugging(message, is_debug, gbf=False):
    if is_debug and not gbf:
        print(message)
    elif is_debug and gbf:
        for m in message:
            point = m.point
            h = m.heuristic
            print(f"Point: {point}, Heuristic: {h}")

def choose_player(turn, player, start_type):
    if turn < 5:
        if turn < 1:
            return "Player 1"
        if start_type in ['Pro', 'Long Pro']:
            if turn < 2:
                return "Player 2"
        if start_type in ['Swap', 'Swap2']:
            if turn < 3:
                return "Player 1"
            elif start_type == 'Swap2':
                return "Player 2"
    return "Player 2" if player == "Player 1" else "Player 1"