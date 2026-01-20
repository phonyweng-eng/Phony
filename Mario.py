import streamlit as st
import random

st.set_page_config(page_title="Mario Game", layout="centered")

# ---------------- STATE ----------------
if "y" not in st.session_state:
    st.session_state.y = 0
    st.session_state.vy = 0
    st.session_state.score = 0
    st.session_state.tick = 0
    st.session_state.dead = False

# ---------------- CONSTANTS ----------------
GROUND = 0
GRAVITY = -1
JUMP = 7
WIDTH = 20

# ---------------- CONTROLS ----------------
st.title("🍄 Mario (HTML Edition)")
st.caption("Jump over enemies • Collect coins")

col1, col2 = st.columns(2)

with col1:
    if st.button("⬆️ Jump") and st.session_state.y == GROUND and not st.session_state.dead:
        st.session_state.vy = JUMP

with col2:
    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()

# ---------------- GAME LOGIC ----------------
if not st.session_state.dead:
    st.session_state.vy += GRAVITY
    st.session_state.y += st.session_state.vy
    st.session_state.tick += 1

if st.session_state.y <= GROUND:
    st.session_state.y = GROUND
    st.session_state.vy = 0

random.seed(st.session_state.tick)

coin = random.randint(6, WIDTH - 2)
enemy = random.randint(10, WIDTH - 1)

player_x = 2

# collision
if st.session_state.y == GROUND:
    if player_x == coin:
        st.session_state.score += 1
    if player_x == enemy:
        st.session_state.dead = True

# ---------------- WORLD RENDER ----------------
world = ["⬜"] * WIDTH
world[coin] = "🪙"
world[enemy] = "👾"
world[player_x] = "🍄"

# ---------------- HTML ----------------
html = f"""
<style>
.game {{
    font-size: 36px;
    background: linear-gradient(#87ceeb, #ffffff);
    padding: 20px;
    border-radius: 12px;
    text-align: center;
}}
.info {{
    font-size: 18px;
    margin-top: 10px;
}}
.dead {{
    color: red;
    font-weight: bold;
}}
</style>

<div class="game">
    <div>{"".join(world)}</div>
    <div class="info">
        Score: {st.session_state.score} <br>
        Height: {st.session_state.y}
    </div>
    {"<div class='dead'>💀 GAME OVER</div>" if st.session_state.dead else ""}
</div>
"""

st.markdown(html, unsafe_allow_html=True)
