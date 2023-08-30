import streamlit as st 
from PIL import Image
from ..chatter import Chatter
from .chat import chat
from .profile_form import profile_form
from ..config import CONFIG

def run_app(chatter: Chatter):
    
    logo = Image.open(
        CONFIG.ASSETS_DIR.joinpath("cute-robot").with_suffix(".png")
    )
    
    with st.sidebar:
        
        # Logo
        st.image(logo)
        st.divider()
        
        # Chatbot's profile
        profile_form()
        
        # A switch determines
        # whether to use domain knowledge, i.e., the notes
        do_use_domain_knowledge = st.toggle("Use Domain Knowledge")
        
        # Set the chatter
        if "chatter" not in st.session_state:
            st.session_state.chatter = chatter
        chatter = st.session_state.chatter
        chatter.do_use_domain_knowledge = do_use_domain_knowledge
        
    chat()
