import streamlit as st
from src.utils import *

with st.sidebar:
    board_size = st.slider("Board Size", 5, 20, 19, 1)
    win_len = st.slider("Winning Length", 3, 10, 5, 1)

st.title("Gomoku Game")

if 'board' not in st.session_state:
    st.session_state.board = [[0 for _ in range(board_size)] for _ in range(board_size)]
    st.session_state.current_player = -1
with st.sidebar:
    st.write("Current Player:")
    st.markdown(marks[st.session_state.current_player])

for i in range(board_size):
    cols = st.columns(board_size)
    for j in range(board_size):
        if cols[j].button("", icon=marks[st.session_state.board[i][j]], key=f"{i}-{j}"):
            make_move(st.session_state.board, i, j, st.session_state.current_player, 0)
            w = check_winner(st.session_state.board, 0, board_size, win_len)
            if w == 1:
                st.session_state.winner = st.session_state.current_player
                st.session_state.board = reset_game(0, board_size)
                st.session_state.current_player = -1
                st.switch_page("src/gameover.py")
            elif w == -1:
                st.session_state.board = reset_game(0, board_size)
                st.session_state.current_player = -1
                st.switch_page("src/gameover.py")
            st.session_state.current_player *= -1
            st.rerun()


with st.sidebar:
    if st.button("Reset Game"):
        st.session_state.board = reset_game(0, board_size)
        st.session_state.current_player = -1
        st.rerun()
