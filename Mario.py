import streamlit as st

st.set_page_config(page_title="Mini Mario", layout="centered")

# --- Game state ---
if "x" not in st.session_state:
    st.session_state.x = 0
    st.session_state.y = 0
    st.session_state.vy = 0
    st.session_state.score = 0

# --- Constants ---
GROUND = 0
GRAVITY = -1
JUMP_POWER = 8

# --- Controls ---
st.title("🍄 Mini Mario (Streamlit Edition)")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("⬅️ Left"):
        st.session_state.x -= 1

with col2:
    if st.button("⬆️ Jump") and st.session_state.y == GROUND:
        st.session_state.vy = JUMP_POWER

with col3:
    if st.button("➡️ Right"):
        st.session_state.x += 1

# --- Physics ---
st.session_state.vy += GRAVITY
st.session_state.y += st.session_state.vy

if st.session_state.y <= GROUND:
    st.session_state.y = GROUND
    st.session_state.vy = 0

# --- Display ---
st.markdown(f"""
### 🧍 Mario Position
- X: **{st.session_state.x}**
- Y: **{st.session_state.y}**
""")

# --- Simple world ---
world = ["🟩"] * 20
pos = max(0, min(19, st.session_state.x + 10))
world[pos] = "🍄"

st.markdown("".join(world))

st.caption("Use the buttons to move Mario")
