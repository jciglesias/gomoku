import streamlit as st
from src.utils import *

st.balloons()
l, r = st.columns(2)
with l.container(border=True):
    if 'winner' not in st.session_state:
        st.title("It's a draw!")
    else:
        st.title(f"Winner: {marks[st.session_state.winner]}")
        del st.session_state['winner']
    # show the final board state
    st.write("Final Board State:")
    if 'board' in st.session_state:
        for row in st.session_state.board:
            st.write(" ".join(marks[cell] for cell in row))
        del st.session_state['board']
with r.container():
    if st.button("Play Again"):
        st.session_state.clear()
        st.switch_page("src/game.py")