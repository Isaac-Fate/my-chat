import typer
from typing import Optional
from typing_extensions import Annotated
from prompt_toolkit import prompt
from rich import print
import tomllib
from .app import app
from ..config import EXISTING_CONFIG_FILEPATH, CONFIG, load_config
from ..schema import (
    ChatRole, 
    UserMessage, 
    AssistantMessage
)

        
USER_AVATAR = "🧐"
ASSISTANT_AVATAR = "🤖"

@app.command()
def chat(
        profile: Annotated[
            Optional[str],
            typer.Option(
                "--profile", "-p",
                help="Profile name"
            )
        ] = None,
    ):

    # Greetings
    print(f"Welcom to the chat room.")
    print(f"Type 'quit' or 'q' to exit the chat room.")
    print()
    
    # Load project configuration settings
    load_config(EXISTING_CONFIG_FILEPATH)
    
    # Load profile
    if profile is None:
        profile = "You are a helpful assistant"
    else:
        profile_name = profile
        with open(CONFIG.CHATTER_PROFILES_FILEPATH, "rb") as f:
            profiles = tomllib.load(f)
        profile = profiles[profile_name]
    
    # Create a chatter
    
    from ..chatter import (
        Chatter,
        ChatHistoryManager,
    )
    from ..note_manager import NoteManager
    from ..notedb import NoteDBClient
    from ..vecdb import VecDBClient
    
    chatter = Chatter(
        profile=profile,
        chat_history_manager=ChatHistoryManager(),
        note_manager=NoteManager(
            note_db_client=NoteDBClient.from_connection_string(
                CONFIG.MONGO_CONNECTION_STRING
            ),
            vec_db_client=VecDBClient.from_connection_string(
                CONFIG.QDRANT_CONNECTION_STRING
            )
        ),
        num_notes_limit=5,
        stream=True
    )

    # Conversation loop
    is_done = False
    while not is_done:
        is_done = have_one_conversation(chatter)

def have_one_conversation(chatter):
    
    # Get user's query   
    query = prompt(f"{USER_AVATAR}: ")
    
    # Check if the user want to quit
    if query.lower().strip() in {"quit", "q"}:
        return True

    # Get response from the chatter
    response = chatter(query)
    
    # Handle stream output
    if chatter.stream:
        
        partial_responses = []
            
        for i, chunk in enumerate(response):
            
            # Print the avatar
            if i == 0:
                print(f"{ASSISTANT_AVATAR}: ", end="")
            
            choice = chunk.choices[0]
            delta = choice.delta
            
            # There is no content in current chunk
            if "content" not in delta:
                continue
            
            # Get the partial response in the chunk
            partial_response = delta.content
            partial_responses.append(partial_response)
            
            # Print the partial response
            print(partial_response, end="")
            
        print()
        
        # Make the complete response
        response = "".join(partial_responses)
        
        # Insert into the chat history manually
        chatter.chat_history_manager.insert_message(
            AssistantMessage(response)
        )
    
    # Handle complete output
    else:
        
        # Print AI's response directly
        print(f"{ASSISTANT_AVATAR}: {response}")
        
    return False
