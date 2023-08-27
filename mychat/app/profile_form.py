import streamlit as st

def submit_assistant_profile(
        assistant_profile: str
    ):
    
    st.session_state.assistant_profile = assistant_profile
    st.session_state.chatter.profile = assistant_profile

def profile_form():
    
    # assistant profile form
    with st.form("assistant_profile_form"):
        
        assistant_profile = st.text_area(
            label="Describe your chatbot:",
            value="",
            placeholder="You are..."
        )
        
        is_submitted = st.form_submit_button(
            label="Set Profile"
        )
        
    if is_submitted:
        submit_assistant_profile(assistant_profile)