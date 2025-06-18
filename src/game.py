import streamlit as st
from src.utils import *
from src.bot import bot_move, bot_suggestion
from src.valid_move import check_valid_move
from time import perf_counter

def change_board_size():
    if st.session_state.mode == "Player vs Player":
        st.session_state.board = reset_game(0, st.session_state.board_size, st.session_state.game_type)
    else:
        st.session_state.board = reset_game(0, st.session_state.board_size, "Classic")
    if 'current_piece' in st.session_state:
        del st.session_state.current_piece
    if 'bot_time' in st.session_state:
        del st.session_state.bot_time
    if 'last_move' in st.session_state:
        del st.session_state.last_move
    if 'turn' in st.session_state:
        del st.session_state.turn
    if 'score' in st.session_state:
        del st.session_state.score
    if 'player' in st.session_state:
        del st.session_state.player
    
def swap_player(next_piece, current_player, turn, game_type):
    chosen_piece = st.pills(f"{current_player} select your piece:", [1,-1], format_func=lambda option: marks[option], selection_mode="single")
    if chosen_piece is not None and chosen_piece != next_piece:
        return choose_player(turn, current_player, game_type)
    elif chosen_piece is None:
        return None
    return current_player

with st.sidebar:
    mode = st.radio("Game Mode", ["Player vs Player", "Player vs Bot"], horizontal=True, key="mode", on_change=change_board_size)
    st.toggle("Suggest Moves", key="suggest_moves", disabled=mode != "Player vs Player")
    board_size = st.slider("Board Size", 5, 20, 19, 1, on_change=change_board_size, key="board_size")
    win_len = st.slider("Winning Length", 3, 10, 5, 1, on_change=change_board_size, key="win_len")
    debug = st.checkbox("Debug Mode", value=False, key="debug")
    type_of_start = st.radio('Choose type of start', ['Classic', 'Pro', 'Long Pro', 'Swap', 'Swap2'], horizontal=True, key="game_type", on_change=change_board_size, disabled=mode == "Player vs Bot")
    game_rules = st.multiselect("Game Rules", ["Capture", "Double Three"], default=["Capture", "Double Three"])
    if mode == "Player vs Bot":
        type_of_start = "Classic"

if 'current_piece' not in st.session_state:
    st.session_state.current_piece = 1 if type_of_start in ['Pro', 'Long Pro'] else -1
if 'turn' not in st.session_state:
    st.session_state.turn = 0 if type_of_start not in ['Pro', 'Long Pro'] else 1
if "player" not in st.session_state:
    st.session_state.player = choose_player(st.session_state.turn, None, type_of_start)

if 'score' not in st.session_state:
    st.session_state.score = {1: 0, -1: 0}
l, m, r = st.columns(3)
with l.container(border=True):
    st.subheader("Current Player:")
    # if st.session_state.turn == 5 and type_of_start == 'Swap2':
    if st.session_state.turn == 3 and type_of_start in ['Swap', 'Swap2']:
        st.session_state.player = swap_player(st.session_state.current_piece, "Player 2", st.session_state.turn, type_of_start)
    st.write(st.session_state.player, marks[st.session_state.current_piece])
with r.container(border=True):
    st.subheader("Score")
    cl, cr = st.columns(2)
    cl.write(f"{marks[1]}: {st.session_state.score.get(1, 0)}")
    cr.write(f"{marks[-1]}: {st.session_state.score.get(-1, 0)}")

m.title("Gomoku Game")

if 'board' not in st.session_state:
    st.session_state.board =  reset_game(0, board_size, type_of_start)
if 'last_move' not in st.session_state:
    st.session_state.last_move = None

if st.session_state.current_piece == -1 and 'bot_time' in st.session_state:
    st.toast(f"Bot made a move in {st.session_state.bot_time:.4f} seconds", icon="🤖")
    st.sidebar.write(f"Bot Time: {st.session_state.bot_time:.4f} seconds")
    del st.session_state.bot_time
points_suggested = bot_suggestion(st.session_state.board, board_size, win_len, st.session_state.current_piece, st.session_state.score, debug, game_rules) if mode == "Player vs Player" and st.session_state.suggest_moves else None
for i in range(board_size):
    cols = st.columns(board_size)
    for j in range(board_size):
        type_button = get_button_type(st.session_state.last_move, i, j,  points_suggested)
        if cols[j].button(
            marks[st.session_state.board[i][j]],
            type=type_button,
            key=f"{i}-{j}", 
            disabled=(st.session_state.current_piece == 1 and mode == "Player vs Bot") or not st.session_state.player
            ):
            if check_valid_move(st.session_state.board, i, j, 0, st.session_state.current_piece, game_rules):
                st.session_state.board = make_move(st.session_state.board, i, j, st.session_state.current_piece, 0, st.session_state.score, game_rules)
                st.session_state.turn += 1
            else:
                st.toast("Invalid move! Please try again.", icon="🚫")
                continue
            w = check_winner(st.session_state.board, 0, board_size, win_len)
            if w == 1 or st.session_state.score[st.session_state.current_piece] >= 5:
                st.session_state.winner = st.session_state.current_piece
                st.session_state.board = reset_game(0, board_size, type_of_start)
                st.session_state.current_piece = -1
                st.switch_page("src/gameover.py")
            elif w == -1:
                st.session_state.board = reset_game(0, board_size, type_of_start)
                st.session_state.current_piece = -1
                st.switch_page("src/gameover.py")
            st.session_state.current_piece *= -1
            st.session_state.last_move = (i, j)
            if 'bot_time' in st.session_state:
                del st.session_state.bot_time
            st.session_state.player = choose_player(st.session_state.turn, st.session_state.player, type_of_start)
            st.rerun()
if st.session_state.current_piece == 1 and mode == "Player vs Bot":
    start_time = perf_counter()
    st.session_state.last_move = bot_move(st.session_state.board, board_size, win_len, st.session_state.turn, st.session_state.score, debug, game_rules)
    end_time = perf_counter()
    st.session_state.board = make_move(st.session_state.board, st.session_state.last_move[0], st.session_state.last_move[1], 1, 0, st.session_state.score, game_rules)
    st.session_state.bot_time = end_time - start_time
    w = check_winner(st.session_state.board, 0, board_size, win_len)
    if w == 1 or st.session_state.score[1] >= 5:
        st.session_state.winner = st.session_state.current_piece
        st.session_state.board = reset_game(0, board_size, type_of_start)
        st.session_state.current_piece = -1
        st.switch_page("src/gameover.py")
    elif w == -1:
        st.session_state.board = reset_game(0, board_size, type_of_start)
        st.session_state.current_piece = -1
        st.switch_page("src/gameover.py")
    else:
        st.session_state.current_piece *= -1
        st.session_state.player = choose_player(st.session_state.turn, st.session_state.player, type_of_start)
        st.rerun()

with st.sidebar:
    st.button("Reset Game", disabled=st.session_state.current_piece == 1 and mode == "Player vs Bot", on_click=change_board_size)
