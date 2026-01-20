import streamlit as st
import pygame
import numpy as np
import time

# --- CONFIGURATION ---
WIDTH, HEIGHT = 600, 400
FPS = 30  # Streamlit works best at lower frame rates

# Colors
SKY_BLUE = (107, 140, 255)
GRASS_GREEN = (34, 177, 76)
MARIO_RED = (255, 0, 0)

# --- INITIALIZE SESSION STATE ---
# We use st.session_state to keep Mario's position alive between reruns
if 'player_pos' not in st.session_state:
    st.session_state.player_pos = [100, 310] # [x, y]
    st.session_state.vel_y = 0
    st.session_state.on_ground = True

# --- UI LAYOUT ---
st.title("🕹️ Streamlit Mario")
st.write("Use the buttons below to control Mario!")

# Create a placeholder for the game screen
game_window = st.empty()

# Create Control Buttons
col1, col2, col3 = st.columns([1,1,1])
with col1:
    move_left = st.button("⬅️ Left")
with col2:
    jump = st.button("🚀 Jump")
with col3:
    move_right = st.button("➡️ Right")

# --- GAME ENGINE ---
def run_frame():
    # 1. Logic & Physics
    if move_left:
        st.session_state.player_pos[0] -= 15
    if move_right:
        st.session_state.player_pos[0] += 15
    if jump and st.session_state.on_ground:
        st.session_state.vel_y = -18
        st.session_state.on_ground = False

    # Apply Gravity
    st.session_state.vel_y += 1.5
    st.session_state.player_pos[1] += st.session_state.vel_y

    # Ground Collision
    if st.session_state.player_pos[1] >= 310:
        st.session_state.player_pos[1] = 310
        st.session_state.vel_y = 0
        st.session_state.on_ground = True

    # 2. Draw using Pygame (Off-screen Surface)
    surface = pygame.Surface((WIDTH, HEIGHT))
    surface.fill(SKY_BLUE)
    
    # Draw Ground
    pygame.draw.rect(surface, GRASS_GREEN, (0, 350, WIDTH, 50))
    
    # Draw Mario (The Red Square)
    mario_rect = pygame.Rect(st.session_state.player_pos[0], st.session_state.player_pos[1], 30, 40)
    pygame.draw.rect(surface, MARIO_RED, mario_rect)

    # 3. Convert Pygame Surface to RGB Array for Streamlit
    img_array = pygame.surfarray.array3d(surface)
    # Pygame uses (width, height, rgb), Streamlit needs (height, width, rgb)
    return np.transpose(img_array, (1, 0, 2))

# Update the display
frame = run_frame()
game_window.image(frame, use_container_width=True)

# Auto-refresh logic (Experimental hack for animation)
if not st.session_state.on_ground:
    time.sleep(0.05)
    st.rerun()
