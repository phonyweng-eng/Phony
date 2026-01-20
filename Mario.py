import streamlit as st
import pygame
import numpy as np
import os

# This line tells Pygame to run without a monitor/window (essential for Streamlit Cloud)
os.environ["SDL_VIDEODRIVER"] = "dummy"

st.title("Streamlit Mario")

# Initialize Pygame
pygame.init()
surface = pygame.Surface((600, 400))

# Game State
if 'x' not in st.session_state:
    st.session_state.x = 100

# Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("Move Left"):
        st.session_state.x -= 20
with col2:
    if st.button("Move Right"):
        st.session_state.x += 20

# Drawing
surface.fill((107, 140, 255)) # Sky
pygame.draw.rect(surface, (255, 0, 0), (st.session_state.x, 300, 30, 40)) # Mario
pygame.draw.rect(surface, (34, 139, 34), (0, 340, 600, 60)) # Ground

# Display in Streamlit
img_array = pygame.surfarray.array3d(surface)
img_array = np.transpose(img_array, (1, 0, 2))
st.image(img_array, use_container_width=True)
