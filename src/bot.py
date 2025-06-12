from src.search_algo import *
from src.utils import *
from src.heuristic import heuristic

def bot_move(board, board_size, win_len, last_move):
    # depth = 10
    # print("Creating tree")
    # best_move_node = ab_minmax(board, -1, depth, 0, win_len, last_move, heuristic, True, float('-inf'), float('inf'))
    # print("tree created")

    # if best_move_node and best_move_node.point:
    #     board = make_move(board, best_move_node.point[0], best_move_node.point[1], 1, 0)
    # return board
    return greedy_best_first(board, board_size, win_len, heuristic)