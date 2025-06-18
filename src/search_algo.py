from src.utils import *

class move:
    point: tuple
    heuristic: int

    def __init__(self, point):
        self.point = point

def greedy_best_first(board, board_size, win_len, heuristic, player, depth_limit=10, score=None, debug=False, game_rules=[]):

    moves = get_possible_moves(board, empty_cell=0)
    if not moves and check_empty_board(board, empty_cell=0):
        return (len(board) // 2, len(board) // 2)
    move_objects = []

    # Score all possible moves using the heuristic
    for m in moves:
        new_board = make_move(board, m[0], m[1], player, empty_cell=0)
        h = heuristic(board_size, win_len, new_board, player, m[0], m[1], score, game_rules)
        mv = move(m)
        mv.heuristic = h
        move_objects.append(mv)

    # Sort by heuristic descending
    move_objects.sort(key=lambda x: x.heuristic, reverse=True)
    debugging(move_objects, debug, True)
    best = move_objects[0]
    for mv in move_objects:
        test_board = make_move(board, mv.point[0], mv.point[1], player, empty_cell=0, game_rules=game_rules)
        debugging(f"First level branch: {mv.point} with heuristic {mv.heuristic}", debug)
        if mv.heuristic < -140:
            break # Skip sure loss moves
        if minmax(test_board, player, -1, depth_limit - 1, board_size, win_len, heuristic, score, debug, game_rules):
            debugging(f"Chose move leading to win/safety: {mv.point}", debug)
            return mv.point

    # If no immediate win found, return the best heuristic move
    return best.point if best else None
    
def minmax(board, player, opponent, depth, board_size, win_len, heuristic, g_score, debug, game_rules):
    if depth <= 0 or check_winner(board, empty_cell=0, board_size=board_size, win_len=win_len):
        debugging(f"Reached level {10 - depth} or found winner", debug)
        # Victory or safe enough
        return True

    op_moves = get_possible_moves(board, empty_cell=0)
    # Heuristically prioritize moves
    op_scored = []
    for m in op_moves:
        test_board = make_move(board, m[0], m[1], opponent, empty_cell=0)
        score = heuristic(board_size, win_len, test_board, opponent, m[0], m[1], g_score, game_rules)
        op_scored.append((score, m))
    op_scored.sort(reverse=True)

    for op_h, op_move in op_scored[:3]:  # Only try top 3 moves for speed
        test_board = make_move(board, op_move[0], op_move[1], opponent, empty_cell=0, game_rules=game_rules)
        debugging(f"Level {10-depth} opponent move: {op_move} with heuristic {op_h}", debug)
        if check_winner(test_board, empty_cell=0, board_size=board_size, win_len=win_len):
            # If opponent can win, we must block
            return False
        moves = get_possible_moves(test_board, empty_cell=0)
        scored = []
        for m in moves:
            board = make_move(test_board, m[0], m[1], player, empty_cell=0)
            score = heuristic(board_size, win_len, board, player, m[0], m[1], g_score, game_rules)
            scored.append((score, m))
        scored.sort(reverse=True)

        if not scored:
            continue

        # If opponent has a strong winning move, abandon path
        for b_h, move in scored[:3]:
            board = make_move(test_board, move[0], move[1], player, empty_cell=0, game_rules=game_rules)
            debugging(f"Level {11-depth} bot move: {move} with heuristic {b_h}", debug)
            if check_winner(board, empty_cell=0, board_size=board_size, win_len=win_len):
                return True

            # Try recursive lookahead
            if minmax(board, player, opponent, depth - 2, board_size, win_len, heuristic, g_score, debug, game_rules):
                return True

    return False

def is_terminal(board, empty_cell, win_len):
    if check_winner(board, empty_cell, len(board), win_len):
        return True
    return False

def get_possible_moves(board, empty_cell, radius=2):
    size = len(board)
    possible_moves = set()

    for i in range(size):
        for j in range(size):
            if board[i][j] != empty_cell:
                for dx in range(-radius, radius + 1):
                    for dy in range(-radius, radius + 1):
                        ni, nj = i + dx, j + dy
                        if 0 <= ni < size and 0 <= nj < size:
                            if board[ni][nj] == empty_cell:
                                possible_moves.add((ni, nj))

    return list(possible_moves)

def first_move(board, player):
    moves = get_possible_moves(board, empty_cell=0, radius=1)
    return moves[0]
