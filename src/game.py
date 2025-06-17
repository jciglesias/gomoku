import streamlit as st
from src.utils import *
from src.bot import bot_move, get_heuristic_board, bot_suggestion
from src.valid_move import check_valid_move
from time import perf_counter

def change_board_size():
    st.session_state.board = reset_game(0, st.session_state.board_size)
    st.session_state.current_player = -1
    if 'bot_time' in st.session_state:
        del st.session_state.bot_time
    if 'last_move' in st.session_state:
        del st.session_state.last_move
    if 'turn' in st.session_state:
        del st.session_state.turn
    if 'score' in st.session_state:
        del st.session_state.score

with st.sidebar:
    mode = st.radio("Game Mode", ["Player vs Player", "Player vs Bot"], horizontal=True, key="mode", on_change=change_board_size)
    if 'current_player' not in st.session_state:
        st.session_state.current_player = -1
    sl, sr = st.columns(2)
    sl.toggle("Suggest Moves", key="suggest_moves", disabled=mode != "Player vs Player")
    sr.write("Current Player:")
    sr.markdown(marks[st.session_state.current_player])
    board_size = st.slider("Board Size", 5, 20, 19, 1, on_change=change_board_size, key="board_size")
    win_len = st.slider("Winning Length", 3, 10, 5, 1, on_change=change_board_size, key="win_len")
    debug = st.checkbox("Debug Mode", value=False, key="debug")

if 'score' not in st.session_state:
    st.session_state.score = {1: 0, -1: 0}
l, r = st.columns(2)
with r.container(border=True):
    st.subheader("Score")
    st.write(f"{marks[1]}: {st.session_state.score.get(1, 0)}")
    st.write(f"{marks[-1]}: {st.session_state.score.get(-1, 0)}")

l.title("Gomoku Game")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
if 'turn' not in st.session_state:
    st.session_state.turn = 0
if 'last_move' not in st.session_state:
    st.session_state.last_move = None

if st.session_state.current_player == -1 and 'bot_time' in st.session_state:
    st.toast(f"Bot made a move in {st.session_state.bot_time:.4f} seconds", icon="🤖")
    st.sidebar.write(f"Bot Time: {st.session_state.bot_time:.4f} seconds")
    del st.session_state.bot_time
# help_board = st.session_state.board if not st.session_state.debug else get_heuristic_board(st.session_state.board, board_size, win_len)
points_suggested = bot_suggestion(st.session_state.board, board_size, win_len, st.session_state.current_player, st.session_state.score, debug) if mode == "Player vs Player" and st.session_state.suggest_moves else None
for i in range(board_size):
    cols = st.columns(board_size)
    for j in range(board_size):
        type_button = get_button_type(st.session_state.last_move, i, j,  points_suggested)
        if cols[j].button(
            marks[st.session_state.board[i][j]],
            type=type_button,
            key=f"{i}-{j}", 
            # help=f"{help_board[i][j]}",
            disabled=st.session_state.current_player == 1 and mode == "Player vs Bot"
            ):
            if check_valid_move(st.session_state.board, i, j, 0, st.session_state.current_player):
                st.session_state.board = make_move(st.session_state.board, i, j, st.session_state.current_player, 0, st.session_state.score)
                st.session_state.turn += 1
            else:
                st.toast("Invalid move! Please try again.", icon="🚫")
                continue
            w = check_winner(st.session_state.board, 0, board_size, win_len)
            if w == 1 or st.session_state.score[st.session_state.current_player] >= 5:
                st.session_state.winner = st.session_state.current_player
                st.session_state.board = reset_game(0, board_size)
                st.session_state.current_player = -1
                st.switch_page("src/gameover.py")
            elif w == -1:
                st.session_state.board = reset_game(0, board_size)
                st.session_state.current_player = -1
                st.switch_page("src/gameover.py")
            st.session_state.current_player *= -1
            st.session_state.last_move = (i, j)
            if 'bot_time' in st.session_state:
                del st.session_state.bot_time
            st.rerun()
if st.session_state.current_player == 1 and mode == "Player vs Bot":
    start_time = perf_counter()
    st.session_state.last_move = bot_move(st.session_state.board, board_size, win_len, st.session_state.turn, st.session_state.score, debug)
    end_time = perf_counter()
    st.session_state.board = make_move(st.session_state.board, st.session_state.last_move[0], st.session_state.last_move[1], 1, 0, st.session_state.score)
    st.session_state.bot_time = end_time - start_time
    w = check_winner(st.session_state.board, 0, board_size, win_len)
    if w == 1 or st.session_state.score[1] >= 5:
        st.session_state.winner = st.session_state.current_player
        st.session_state.board = reset_game(0, board_size)
        st.session_state.current_player = -1
        st.switch_page("src/gameover.py")
    elif w == -1:
        st.session_state.board = reset_game(0, board_size)
        st.session_state.current_player = -1
        st.switch_page("src/gameover.py")
    else:
        st.session_state.current_player *= -1
        st.rerun()

with st.sidebar:
    if st.button("Reset Game", disabled=st.session_state.current_player == 1 and mode == "Player vs Bot", on_click=change_board_size):
        st.rerun()
