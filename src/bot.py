from src.minmax import ab_minmax, create_tree
from src.utils import *
from src.heuristic import heuristic

def bot_move(board, board_size, win_len, last_move):

    depth = 10

    print("Creating tree")
    root = create_tree(board, -1, depth, 0, win_len, last_move)
    print("tree created")
    best_move_node = ab_minmax(root, depth, False, float('-inf'), float('inf'), heuristic)

    if best_move_node and best_move_node.point:
        board = make_move(board, best_move_node.point[0], best_move_node.point[1], 1, 0)
    
    return board