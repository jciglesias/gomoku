from src.search_algo import *
from src.utils import *
from src.heuristic import heuristic

def bot_move(board, board_size, win_len, turn):
    depth = 10
    player = 1
    if turn == 1:
        return first_move(board, player)
    return greedy_best_first(board, board_size, win_len, heuristic,  player, depth)

def get_heuristic_board(board, board_size, win_len):
    heuristic_board = []
    for i in range(board_size):
        row = []
        for j in range(board_size):
            if board[i][j] == 0:
                new_board = make_move(board, i, j, 1, 0)
                h = heuristic(board_size, win_len, new_board, 1)
                row.append(str(h))
            else:
                row.append(marks[board[i][j]])
        heuristic_board.append(row)
    return heuristic_board