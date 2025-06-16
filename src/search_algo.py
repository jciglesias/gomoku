from src.utils import make_move, check_winner

class move:
    point: tuple
    heuristic: int

    def __init__(self, point):
        self.point = point

def greedy_best_first(board, board_size, win_len, heuristic, player, depth_limit=10):

    moves = get_possible_moves(board, empty_cell=0)
    move_objects = []

    # Score all possible moves using the heuristic
    for m in moves:
        new_board = make_move(board, m[0], m[1], player, empty_cell=0)
        h = heuristic(board_size, win_len, new_board, player)
        mv = move(m)
        mv.heuristic = h
        move_objects.append(mv)

    # Sort by heuristic descending
    move_objects.sort(key=lambda x: x.heuristic, reverse=True)
    print("Possible moves with heuristics:")
    for mv in move_objects:
        print(f"Move: {mv.point}, Heuristic: {mv.heuristic}")

    # Try moves in order of best heuristic; use alpha-beta to see if it's winning
    for mv in move_objects:
        test_board = make_move(board, mv.point[0], mv.point[1], player, empty_cell=0)
        if minmax(test_board, player, -1, depth_limit - 1, board_size, win_len, heuristic):
            print(f"Chose move leading to win/safety: {mv.point}")
            return make_move(board, mv.point[0], mv.point[1], player, empty_cell=0)

    # If no immediate win found, return the best heuristic move
    best = move_objects[0]
    return make_move(board, best.point[0], best.point[1], player, empty_cell=0)
    
def minmax(board, player, opponent, depth, board_size, win_len, heuristic):
    if depth <= 0 or check_winner(board, empty_cell=0, board_size=board_size, win_len=win_len):
        # Victory or safe enough
        return True

    moves = get_possible_moves(board, empty_cell=0)
    # Heuristically prioritize moves
    scored = []
    for m in moves:
        test_board = make_move(board, m[0], m[1], player, empty_cell=0)
        score = heuristic(board_size, win_len, test_board, player)
        scored.append((score, m))
    scored.sort(reverse=True)

    for _, move in scored[:3]:  # Only try top 3 moves for speed
        test_board = make_move(board, move[0], move[1], player, empty_cell=0)
        # Simulate opponent’s best response
        opp_moves = get_possible_moves(test_board, empty_cell=0)
        opp_scored = []
        for om in opp_moves:
            opp_board = make_move(test_board, om[0], om[1], opponent, empty_cell=0)
            opp_score = heuristic(board_size, win_len, opp_board, opponent)
            opp_scored.append((opp_score, om))
        opp_scored.sort(reverse=True)

        if not opp_scored:
            continue

        # If opponent has a strong winning move, abandon path
        for _, opp_move in opp_scored[:3]:
            opp_board = make_move(test_board, opp_move[0], opp_move[1], opponent, empty_cell=0)
            if check_winner(opp_board, empty_cell=0, board_size=board_size, win_len=win_len):
                return False

            # Try recursive lookahead
            if minmax(opp_board, player, opponent, depth - 2, board_size, win_len, heuristic):
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
    return make_move(board, moves[0][0], moves[0][1], player, empty_cell=0) if moves else board
