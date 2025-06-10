import streamlit as st

st.set_page_config(page_title="Gomoku Game", layout="wide")
home = st.Page('src/game.py', title="Gomoku Game")
gameover = st.Page('src/gameover.py', title="Game Over")
pg = st.navigation([home, gameover], position="hidden")
pg.run()