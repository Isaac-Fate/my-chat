import os
from pathlib import Path
import click

from mychat.config import CONFIG, load_config
from mychat.note_manager import NoteManager
from mychat.notedb import NoteDBClient
from mychat.vecdb import VecDBClient

# Load configuration file
load_config("config.toml")

@click.command()
@click.argument("src", type=click.Path(exists=True))
@click.option(
    "-e", "--ext",
    default="md", 
    show_default=True,
    help="Extension of the note files"
)
def insert_notes(src: os.PathLike, ext: str):
    
    # Directory of the note files
    notes_dir = Path(src)
    
    # Note manager that communicates with
    # the document and vector databases
    note_manager = NoteManager(
        note_db_client=NoteDBClient.from_connection_string(
            CONFIG.MONGO_CONNECTION_STRING
        ),
        vec_db_client=VecDBClient.from_connection_string(
            CONFIG.QDRANT_CONNECTION_STRING
        )
    )
    
    # Clean up databases
    note_manager.note_db_client.drop_collection()
    note_manager.vec_db_client.drop_collection()
    
    # Extension of the note files to insert
    note_file_extension = ext.lower()
    
    # Insert notes
    match note_file_extension:
        case "md" | "markdown":
            note_manager.insert_markdown_notes_under_dir(notes_dir)
        
        case "txt" | "text":
            note_manager.insert_txt_notes_under_dir(notes_dir)
    
if __name__ == "__main__":
    insert_notes()
