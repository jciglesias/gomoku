import streamlit as st
from src.utils import marks

if 'winner' not in st.session_state:
    st.write("It's a draw!")
else:
    st.write(f"Winner: {marks[st.session_state.winner]}")
    del st.session_state['winner']
if st.button("Play Again"):
    st.session_state.clear()
    st.switch_page("src/game.py")