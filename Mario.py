import streamlit as st
import random

st.set_page_config(page_title="Mario Streamlit", layout="centered")

# ---------- INIT ----------
if "player_y" not in st.session_state:
    st.session_state.player_y = 0
    st.session_state.vy = 0
    st.session_state.world_x = 0
    st.session_state.score = 0
    st.session_state.game_over = False

# ---------- CONSTANTS ----------
GROUND = 0
GRAVITY = -1
JUMP_POWER = 8
WORLD_WIDTH = 30

# ---------- TITLE ----------
st.title("🍄 Mario (Streamlit Edition)")
st.caption("Jump on coins. Avoid enemies.")

# ---------- CONTROLS ----------
col1, col2 = st.columns(2)

with col1:
    if st.button("⬆️ Jump") and st.session_state.player_y == GROUND and not st.session_state.game_over:
        st.session_state.vy = JUMP_POWER

with col2:
    if st.button("🔄 Restart"):
        st.session_state.clear()
        st.rerun()

# ---------- PHYSICS ----------
if not st.session_state.game_over:
    st.session_state.vy += GRAVITY
    st.session_state.player_y += st.session_state.vy
    st.session_state.world_x += 1

if st.session_state.player_y <= GROUND:
    st.session_state.player_y = GROUND
    st.session_state.vy = 0

# ---------- WORLD GENERATION ----------
random.seed(st.session_state.world_x)

world = ["🟩"] * WORLD_WIDTH
player_pos = 5

coin_pos = random.randint(10, 20)
enemy_pos = random.randint(15, 25)

# Coin
if coin_pos < WORLD_WIDTH:
    world[coin_pos] = "🪙"

# Enemy
if enemy_pos < WORLD_WIDTH:
    world[enemy_pos] = "☠️"

# Player
world[player_pos] = "🍄"

# ---------- COLLISIONS ----------
if st.session_state.player_y == GROUND:
    if player_pos == coin_pos:
        st.session_state.score += 1
    if player_pos == enemy_pos:
        st.session_state.game_over = True

# ---------- DISPLAY ----------
st.markdown("".join(world))

st.markdown(f"""
**Score:** {st.session_state.score}  
**Height:** {st.session_state.player_y}
""")

if st.session_state.game_over:
    st.error("💀 GAME OVER")
    st.caption("Press Restart to play again")
