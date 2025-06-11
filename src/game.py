import streamlit as st
from src.utils import *

empty_cell = ':material/radio_button_unchecked:'
x_cell = ':material/cancel:'
o_cell = ':material/check_circle:'

with st.sidebar:
    board_size = st.slider("Board Size", 5, 20, 19, 1)
    win_len = st.slider("Winning Length", 3, 10, 5, 1)

st.title("Gomoku Game")

if 'board' not in st.session_state:
    st.session_state.board = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    st.session_state.current_player = x_cell
with st.sidebar:
    st.write("Current Player:")
    st.markdown(st.session_state.current_player)

for i in range(board_size):
    cols = st.columns(board_size)
    for j in range(board_size):
        if cols[j].button("", icon=st.session_state.board[i][j], key=f"{i}-{j}"):
            make_move(st.session_state.board, i, j, st.session_state.current_player, empty_cell)
            w = check_winner(st.session_state.board, empty_cell, board_size, win_len)
            if w == 1:
                st.session_state.winner = st.session_state.current_player
                st.session_state.board = reset_game(empty_cell, board_size)
                st.session_state.current_player = x_cell
                st.switch_page("src/gameover.py")
            elif w == -1:
                st.session_state.board = reset_game(empty_cell, board_size)
                st.session_state.current_player = x_cell
                st.switch_page("src/gameover.py")
            st.session_state.current_player = o_cell if st.session_state.current_player == x_cell else x_cell
            st.rerun()


with st.sidebar:
    if st.button("Reset Game"):
        st.session_state.board = reset_game(empty_cell, board_size)
        st.session_state.current_player = x_cell
        st.rerun()
