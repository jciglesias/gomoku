import streamlit as st

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

def make_move(row, col):
    if st.session_state.board[row][col] == empty_cell:
        st.session_state.board[row][col] = st.session_state.current_player
        st.session_state.current_player = o_cell if st.session_state.current_player == x_cell else x_cell
        check_winner()
        st.rerun()

def check_winner():
    # Check rows, columns, and diagonals for a winning condition
    for i in range(board_size):
        for j in range(board_size):
            if st.session_state.board[i][j] != empty_cell:
                if check_direction(i, j, 1, 0) or check_direction(i, j, 0, 1) or \
                   check_direction(i, j, 1, 1) or check_direction(i, j, 1, -1):
                    st.session_state.winner = st.session_state.board[i][j]
                    reset_game()
                    st.switch_page("src/gameover.py")
    if all(st.session_state.board[i][j] != empty_cell for i in range(board_size) for j in range(board_size)):
        reset_game()
        st.switch_page("src/gameover.py")

def check_direction(row, col, delta_row, delta_col):
    count = 0
    for k in range(win_len):
        r = row + k * delta_row
        c = col + k * delta_col
        if 0 <= r < board_size and 0 <= c < board_size and st.session_state.board[r][c] == st.session_state.board[row][col]:
            count += 1
        else:
            break
    return count == win_len

def reset_game():
    st.session_state.board = [[empty_cell for _ in range(board_size)] for _ in range(board_size)]
    st.session_state.current_player = x_cell

for i in range(board_size):
    cols = st.columns(board_size)
    for j in range(board_size):
        if cols[j].button("", icon=st.session_state.board[i][j], key=f"{i}-{j}"):
            make_move(i, j)

with st.sidebar:
    if st.button("Reset Game"):
        reset_game()
        st.rerun()
