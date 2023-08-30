import streamlit as st
from ..schema import (
    ChatRole, 
    UserMessage, 
    AssistantMessage
)
from ..chatter import (
    Chatter,
    ChatHistoryManager,
)
from ..note_manager import NoteManager
from ..notedb import NoteDBClient
from ..vecdb import VecDBClient

def get_avatar(role: ChatRole) -> str:
    
    match role:
        case ChatRole.User:
            return "😉"
        case ChatRole.Assistant:
            return "🤖"

def chat():

    # App title
    st.title("💕 Yuri's Chatbot 🤖")
    
    # Get the chatter
    assert hasattr(st.session_state, "chatter")
    chatter = st.session_state.chatter
    
    # Load history messages
    if "messages" not in st.session_state:
        st.session_state.messages = []
    history_messages = st.session_state.messages

    # Print history
    for message in history_messages:
        role_name = message["role"]
        content = message["content"]
        role = ChatRole.from_str(role_name)
        with st.chat_message(name=role_name, avatar=get_avatar(role)):
            st.markdown(content)

    # Get user's query   
    query = st.chat_input("I want to ask...")

    if query is not None:
        
        # Print user's query
        with st.chat_message(name=str(ChatRole.User), avatar=get_avatar(ChatRole.User)):
            st.markdown(query)
            
        # Add query to history message
        history_messages.append(UserMessage(query).to_dict())
        
        # Get response from the chatter
        response = chatter(query)
        
        # Handle stream output
        if chatter.stream:
            
            with st.chat_message(name=str(ChatRole.Assistant), avatar=get_avatar(ChatRole.Assistant)):
                
                message_placeholder = st.empty()
                partial_responses = []
                
                for chunk in response:
                    
                    choice = chunk.choices[0]
                    delta = choice.delta
                    
                    # There is no content in current chunk
                    if "content" not in delta:
                        continue
                    
                    # Get the partial response in the chunk
                    partial_response = delta.content
                    partial_responses.append(partial_response)
                    
                    # Print the partial response
                    message_placeholder.markdown("".join(partial_responses))
            
            # Make the complete response
            response = "".join(partial_responses)
            
            # Insert into the chat history manually
            chatter.chat_history_manager.insert_message(
                AssistantMessage(response)
            )
            
        # Handle complete output
        else:
            
            # Print AI's response directly
            with st.chat_message(name=str(ChatRole.Assistant), avatar=get_avatar(ChatRole.Assistant)):
                st.markdown(response)
            
        # Add query to history message
        history_messages.append(AssistantMessage(content=response).to_dict())
