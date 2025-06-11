from src.utils import make_move, check_winner, switch_player

class node:
    
    def __init__(self, point, heuristic, player, is_terminal=False):
        self.point: tuple = point
        self.heuristic: int = heuristic
        self.children = []
        self.is_terminal = is_terminal
        self.player = player

    def add_child(self, child_node):
        self.children.append(child_node)
    
    def __lt__(self, other):
        return self.heuristic < other.heuristic
    
    def __eq__(self, other):
        return self.point == other.point and self.heuristic == other.heuristic

def ab_minmax(node: node, depth: int, maximizing_player: bool, alpha, beta)-> node:
    if depth == 0 or node.is_terminal:
        return node
    
    if maximizing_player:
        max_eval = float('-inf')
        best_node = None
        for child in node.children:
            eval_node = ab_minmax(child, depth - 1, False, alpha, beta)
            if eval_node.heuristic > max_eval:
                max_eval = eval_node.heuristic
                best_node = child
            alpha = max(alpha, eval_node.heuristic)
            if beta <= alpha:
                break
        return best_node
    else:
        min_eval = float('inf')
        best_node = None
        for child in node.children:
            eval_node = ab_minmax(child, depth - 1, True, alpha, beta)
            if eval_node.heuristic < min_eval:
                min_eval = eval_node.heuristic
                best_node = child
            beta = min(beta, eval_node.heuristic)
            if beta <= alpha:
                break
        return best_node

def create_tree(board, player, depth, heuristic_function, empty_cell):
    root = node(point=None, heuristic=0, player=player)
    if depth == 0 or is_terminal(board, player, empty_cell):
        root.heuristic = heuristic_function(board, player, empty_cell)
        root.is_terminal = True
        return root
    for move in get_possible_moves(board, empty_cell):
        new_board = make_move(board, move, player, empty_cell)
        child_node = create_tree(new_board, switch_player(player), depth - 1, heuristic_function, empty_cell)
        child_node.point = move
        child_node.player = player
        root.add_child(child_node)
    return root

def is_terminal(board, player, empty_cell):
    if check_winner(board, player):
        return True
    if all(cell != empty_cell for row in board for cell in row):
        return True
    return False

def get_possible_moves(board, empty_cell):
    possible_moves = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == empty_cell:
                possible_moves.append((i, j))
    return possible_moves

 