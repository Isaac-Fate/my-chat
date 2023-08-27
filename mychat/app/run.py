import streamlit as st 
from PIL import Image
from ..chatter import Chatter
from .chat import chat
from .profile_form import profile_form
from ..config import CONFIG

def run_app(chatter: Chatter):
    
    logo = Image.open(
        CONFIG.ASSETS_DIR.joinpath("robot").with_suffix(".jpg")
    )
    
    with st.sidebar:
        st.image(logo)
        st.divider()
        profile_form()
        
    chat(chatter)
