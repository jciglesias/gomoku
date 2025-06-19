import streamlit as st
from src.utils import *
import math

st.balloons()
l, r = st.columns(2)
with l.container(border=True):
    if 'winner' not in st.session_state:
        st.title("It's a draw!")
    else:
        st.title(f"Winner: {marks[st.session_state.winner]}")
        del st.session_state['winner']
    if 'turn' in st.session_state:
        st.write(f"In {math.ceil(st.session_state.turn/2)} turns")
    st.write("Final Board State:")
    if 'board' in st.session_state:
        for row in st.session_state.board:
            st.write(" ".join(marks[cell] for cell in row))
        del st.session_state['board']
with r.container():
    if st.button("Play Again"):
        st.session_state.clear()
        st.switch_page("src/game.py")