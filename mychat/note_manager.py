import os
from pathlib import Path
from .notedb import NoteDBClient
from .vecdb import VecDBClient
from .schema import Note
from .openai_utils import openai_encode_text

class NoteManager:
    
    def __init__(
            self,
            note_db_client: NoteDBClient,
            vec_db_client: VecDBClient
        ) -> None:
        
        self._note_db_client = note_db_client
        self._vec_db_client = vec_db_client
    
    @property
    def note_db_client(self) -> NoteDBClient:
        return self._note_db_client
    
    @property
    def vec_db_client(self) -> VecDBClient:
        return self._vec_db_client
        
    def insert_note(self, note: Note) -> None:
        
        # Read note content
        with open(note.filepath, "r") as f:
            note_content = f.read()
            
        # Embed the note to a vector
        note_vec = openai_encode_text(note_content)
        
        # Insert the note vector to vector database, and
        # then get the vector ID
        note_vec_id = self._vec_db_client.insert_note_vec(note_vec)
        
        # Set the vector ID
        note.vec_id = note_vec_id
        
        # Insert the note to document database
        self._note_db_client.insert_note(note)
        
    def retrieve_similar_notes(self, query: str, limit: int = 5) -> list[Note]:
        
        # Embed the query to vector
        query_vec = openai_encode_text(query)
        
        # Retrieve the vector IDs of the similar notes
        note_vec_ids = self._vec_db_client.retrieve_similar_note_vec_ids(query_vec, limit)
        
        # Get the corresponding notes
        notes = self._note_db_client.find_notes_by_vec_ids(note_vec_ids)
        
        return notes
    
    def insert_note_from_file(self, filepath: os.PathLike) -> None:
        
        # Convert to a Note instance
        note = Note(filepath)
        
        # Insert note
        self.insert_note(note)
            
    def insert_markdown_notes_under_dir(self, dir: os.PathLike) -> None:
        
        # Convert to a Path instance
        md_dir = Path(dir).absolute()
        
        # Insert all markdown notes
        for md_filepath in md_dir.rglob("*.md"):
            self.insert_note_from_file(md_filepath)
    
    def insert_txt_notes_under_dir(self, dir: os.PathLike) -> None:
        
        # Convert to a Path instance
        md_dir = Path(dir).absolute()
        
        # Insert all markdown notes
        for md_filepath in md_dir.rglob("*.txt"):
            self.insert_note_from_file(md_filepath)
    
    def retrieve_similar_note_contents(self, query: str, limit: int = 5) -> list[str]:
        
        # Retrieve similar notes
        notes = self.retrieve_similar_notes(query, limit)
        
        # Read note contents
        note_contents = []
        for note in notes:
            with open(note.filepath, "r") as f:
                note_content = f.read()
            note_contents.append(note_content)
            
        return note_contents
