from mychat.config import load_config, CONFIG
from mychat.app import run_app
from mychat.chatter import Chatter, ChatHistoryManager
from mychat.note_manager import NoteManager
from mychat.notedb import NoteDBClient
from mychat.vecdb import VecDBClient

if __name__ == "__main__":
    
    # Load configuration file
    load_config("config.toml")
    
    chatter = Chatter(
        profile=(
            "You are a helpful assistant who is going to "
            "answer my question through chatting with me."
        ),
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
    
    # run the app
    run_app(chatter)
    
    