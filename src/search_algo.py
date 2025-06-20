from src.utils import *
from src.valid_move import check_valid_move
import functools

class move:
    point: tuple
    heuristic: int

    def __init__(self, point):
        self.point = point

@functools.lru_cache
def get_win_score(win_len):
    return 10**(2 * win_len - 5) * 0.99

@functools.lru_cache
def get_lost_score(win_len):
    return 10**(2*(win_len-1)-6)*-1.4

def greedy_best_first(board, board_size, win_len, heuristic, player, depth_limit=10, score=None, debug=False, game_rules=[]):

    moves = get_possible_moves(board, empty_cell=0)
    if not moves and check_empty_board(board, empty_cell=0):
        return (len(board) // 2, len(board) // 2)
    move_objects = []

    for m in moves:
        if not check_valid_move(board, m[0], m[1], empty_cell=0, player=player, game_rules=game_rules):
            debugging(f"Skipping invalid move {m} for player {player}", debug)
            continue
        new_board = make_move(board, m[0], m[1], player, empty_cell=0)
        h = heuristic(board_size, win_len, new_board, player, m[0], m[1], score, game_rules)
        mv = move(m)
        mv.heuristic = h
        move_objects.append(mv)

    move_objects.sort(key=lambda x: x.heuristic, reverse=True)
    debugging(move_objects, debug, True)
    counting = 0
    for mv in move_objects:
        test_board = make_move(board, mv.point[0], mv.point[1], player, empty_cell=0, game_rules=game_rules)
        debugging(f"First level branch: {mv.point} with heuristic {mv.heuristic}", debug)
        if mv.heuristic < get_lost_score(win_len):
            break
        if alphabetapruning(test_board, player, -1, depth_limit - 1, board_size, win_len, heuristic, score, debug, game_rules):
            debugging(f"Chose move leading to win/safety: {mv.point}", debug)
            return mv.point
        counting += 1
        if counting >= 10:
            debugging("Reached depth limit of 10 moves", debug)
            break

    best = move_objects[0]
    return best.point if best else None
    
def alphabetapruning(board, alpha, beta, depth, board_size, win_len, heuristic, g_score, debug, game_rules):
    if depth <= 0 or check_winner(board, empty_cell=0, board_size=board_size, win_len=win_len):
        debugging(f"Reached level {10 - depth} or found winner", debug)
        return True

    op_moves = get_possible_moves(board, empty_cell=0)
    op_scored = []
    for m in op_moves:
        test_board = make_move(board, m[0], m[1], beta, empty_cell=0)
        score = heuristic(board_size, win_len, test_board, beta, m[0], m[1], g_score, game_rules)
        op_scored.append((score, m))
    op_scored.sort(reverse=True)

    for op_h, op_move in op_scored[:3]:
        test_board = make_move(board, op_move[0], op_move[1], beta, empty_cell=0, game_rules=game_rules)
        debugging(f"Level {10-depth} beta move: {op_move} with heuristic {op_h}", debug)
        if op_h > get_win_score(win_len):
            debugging(f"Skipping beta move {op_move} with heuristic {op_h}", debug)
            break
        if check_winner(test_board, empty_cell=0, board_size=board_size, win_len=win_len):
            return False
        moves = get_possible_moves(test_board, empty_cell=0)
        scored = []
        for m in moves:
            board = make_move(test_board, m[0], m[1], alpha, empty_cell=0)
            score = heuristic(board_size, win_len, board, alpha, m[0], m[1], g_score, game_rules)
            scored.append((score, m))
        scored.sort(reverse=True)

        if not scored:
            continue

        for b_h, move in scored[:3]:
            board = make_move(test_board, move[0], move[1], alpha, empty_cell=0, game_rules=game_rules)
            debugging(f"Level {11-depth} bot move: {move} with heuristic {b_h}", debug)
            if b_h < get_lost_score(win_len):
                debugging(f"Skipping move {move} with heuristic {b_h}", debug)
                break
            if check_winner(board, empty_cell=0, board_size=board_size, win_len=win_len):
                return True

            if alphabetapruning(board, alpha, beta, depth - 2, board_size, win_len, heuristic, g_score, debug, game_rules):
                return True

    return False

def is_terminal(board, empty_cell, win_len):
    if check_winner(board, empty_cell, len(board), win_len):
        return True
    return False

def first_move(board, player):
    moves = get_possible_moves(board, empty_cell=0, radius=1)
    return moves[0]
