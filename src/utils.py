from copy import deepcopy

marks = {
    0: ':material/radio_button_unchecked:',
    1: ':red[:material/cancel:]',
    -1: ':green[:material/check_circle:]'
}

b_marks = {
    1: ':red-badge[:material/cancel:]',
    -1: ':green-badge[:material/check_circle:]'
}

hint_marks = {
    0: ':gray-background[:material/radio_button_unchecked:]',
    1: ':red-background[:material/cancel:]',
    -1: ':green-background[:material/check_circle:]'
}

hint_marks = {
    0: ':gray-background[:material/radio_button_unchecked:]',
    1: ':red-background[:material/cancel:]',
    -1: ':green-background[:material/check_circle:]'
}

def check_avoid_capture(board, row, col, player):
    board_size = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row - dr, col - dc
        if 0 <= r < board_size and 0 <= c < board_size:
            if board[r][c] != player:
                r2, c2 = row + dr, col + dc
                if 0 <= r2 < board_size and 0 <= c2 < board_size:
                    if board[r2][c2] == player:
                        r3, c3 = r2 + dr, c2 + dc
                        if 0 <= r3 < board_size and 0 <= c3 < board_size:
                            if board[r3][c3] == -player:
                                return True

    return False

def check_alignement_capture(board, row, col, player):
    board_size = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < board_size and 0 <= c < board_size:
            if board[r][c] == -player: 
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < board_size and 0 <= c2 < board_size:
                    if board[r2][c2] == -player:
                        r3, c3 = r2 + dr, c2 + dc
                        if 0 <= r3 < board_size and 0 <= c3 < board_size:
                            if board[r3][c3] == player:
                                return True
    return False

def check_block(board, row, col, empty_cell, player):
    board_size = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < board_size and 0 <= c < board_size and  board[r][c] == -player: 
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < board_size and 0 <= c2 < board_size and board[r2][c2] == -player:
                        return 1
    return 0

def check_capture(board, row, col, empty_cell, player):
    if board[row][col] != empty_cell:
        return False
    return check_alignement_capture(board, row, col, player)

def remove_captured(board, row, col, empty_cell, player):
    board_size = len(board)
    directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    count_captured = 0
    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < board_size and 0 <= c < board_size:
            if board[r][c] == -player:
                r2, c2 = r + dr, c + dc
                if 0 <= r2 < board_size and 0 <= c2 < board_size:
                    if board[r2][c2] == -player:
                        r3, c3 = r2 + dr, c2 + dc
                        if 0 <= r3 < board_size and 0 <= c3 < board_size:
                            if board[r3][c3] == player:
                                count_captured += 1
                                board[r][c] = empty_cell
                                board[r2][c2] = empty_cell
    return board, count_captured

def make_move(board_og, row, col, player, empty_cell, score=None, game_rules=[], turn=0) -> list:
    board = deepcopy(board_og)
    is_capture = check_capture(board, row, col, empty_cell, player)
    if board[row][col] == empty_cell:
        board[row][col] = player
        if is_capture and 'Capture' in game_rules:
            board, n_captures = remove_captured(board, row, col, empty_cell, player)
            if score is not None:
                score[player] +=  n_captures
    if turn > 1:
        if is_capture:
            is_block = 1
        else:
            is_block = check_block(board, row, col, empty_cell, player)
        if score is not None:
            score[2 * player] = round((is_block + score[2 * player] * turn) / (turn + 1), 1)
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
        center = board_size // 2
        board = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
        board[center][center] = -1
        return board
    
def switch_player(player):
    return player * -1

def get_button_type(last_move, i, j, suggestion=None):
    if suggestion and (i, j) in suggestion:
        return "primary"
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

def choose_player(turn, player, start_type, swap=None):
    if turn < 3:
        if start_type in ['Swap', 'Swap2']:
            return "Player 1"
        elif start_type in ['Pro', 'Long Pro']:
            if turn < 2:
                return "Player 2"
        elif turn < 1:
            return "Player 1"
    elif swap and turn < 5:
        return "Player 2"
    return "Player 2" if player == "Player 1" else "Player 1"

def format_value(x):
    if x == int(x):
        return f"{int(x):,}".replace(",", " ")
    else:
        return f"{x:.10f}".rstrip('0').rstrip('.').replace(",", " ")

def find_gray_pro_zone(board, board_size, zone_size):
    moves = get_possible_moves(board, empty_cell=0, radius=zone_size, piece=-1)
    return moves if moves else []

def get_possible_moves(board, empty_cell, radius=1, piece=None):
    size = len(board)
    possible_moves = set()

    for i in range(size):
        for j in range(size):
            if (not piece and board[i][j] != empty_cell) or (piece and board[i][j] == piece):
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < size and 0 <= nj < size:
                            if board[ni][nj] == empty_cell:
                                possible_moves.add((ni, nj))

    return list(possible_moves)