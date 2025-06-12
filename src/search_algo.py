from src.utils import make_move, check_winner, switch_player

class node:
    
    def __init__(self, point, board, player, win_len, is_terminal=False):
        self.point: tuple = point
        self.board: list = board
        # self.children = []
        self.is_terminal = is_terminal
        self.player = player
        self.win_len = win_len

    # def add_child(self, child_node):
    #     self.children.append(child_node)
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    
    def __eq__(self, other):
        return self.point == other.point and self.heuristic == other.heuristic

class move:
    point: tuple
    heuristic: int

    def __init__(self, point):
        self.point = point

# merge ab_minmax and create_tree into a single function
def ab_minmax(
        board: list,
        player: int,
        depth: int,
        empty_cell: int,
        win_len: int,
        point: tuple,
        heuristic: callable,
        maximizing_player: bool = True,
        alpha: float = float('-inf'),
        beta: float = float('inf')
    ) -> node:
    current_node = node(point=point, board=board, player=player, win_len=win_len)
    if depth == 0 or check_winner(board, empty_cell, len(board), win_len):
        current_node.is_terminal = True
        return current_node
    if maximizing_player:
        max_eval = float('-inf')
        best_node = None
        for move in get_possible_moves(board, empty_cell):
            new_player = switch_player(player)
            new_board = make_move(board, move[0], move[1], new_player, empty_cell)
            eval_node = ab_minmax(new_board, new_player, depth - 1, empty_cell, win_len, move, heuristic, False, alpha, beta)
            heuristic_value = heuristic(len(board), win_len, new_board, new_player)
            if heuristic_value > max_eval:
                max_eval = heuristic_value
                best_node = eval_node
            alpha = max(alpha, heuristic_value)
            if beta <= alpha:
                break
        current_node.is_terminal = False
        return best_node if best_node else current_node
    else:
        min_eval = float('inf')
        best_node = None
        for move in get_possible_moves(board, empty_cell):
            new_player = switch_player(player)
            new_board = make_move(board, move[0], move[1], new_player, empty_cell)
            eval_node = ab_minmax(new_board, new_player, depth - 1, empty_cell, win_len, move, heuristic, True, alpha, beta)
            heuristic_value = heuristic(len(board), win_len, new_board, new_player)
            if heuristic_value < min_eval:
                min_eval = heuristic_value
                best_node = eval_node
            beta = min(beta, heuristic_value)
            if beta <= alpha:
                break
        current_node.is_terminal = False
        return best_node if best_node else current_node

def greedy_best_first(board, board_size, win_len, heuristic):
    moves = get_possible_moves(board, 0)
    best_move = move(moves.pop())
    best_move.heuristic = heuristic(board_size, win_len, board, 1)
    for m in moves:
        new_board = make_move(board, m[0], m[1], 1, 0)
        h = heuristic(board_size, win_len, new_board, 1)
        if h > best_move.heuristic:
            best_move.point = m
            best_move.heuristic = h
    return make_move(board, best_move.point[0], best_move.point[1], 1, 0)

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


 