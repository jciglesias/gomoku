directions = [(-1, -1),
            (-1, 0),
            (-1, 1),
            (0, -1),
            (0, 1),
            (1, -1),
            (1, 0),
            (1, 1)
            ]

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

def check_capture(board, row, col, empty_cell, player):
    for i in range(8):
        r = row  + directions[i][0]
        c = col + directions[i][1]
        if 0 <= r < len(board) and 0 <= c < len(board):
                if board[r][c] == -player:
                        r = row - directions[i][0]
                        c = col - directions[i][1]
                        if 0 <= r < len(board) and 0 <= c < len(board):
                                if board[r][c] == player:
                                        r = row  - directions[i][0] * 2
                                        c = col - directions[i][1] * 2
                                        if 0 <= r < len(board) and 0 <= c < len(board):
                                                if board[r][c] == -player:
                                                        return True
    return False

def check_valid_move(board, row, col, empty_cell, player):
    if board[row][col] != empty_cell:
        return False
    if check_capture(board, row, col, empty_cell, player):
        return False
    # check if the move creates a double-three
    if check_threes(board, row, col, empty_cell, player):
        return False
    return True