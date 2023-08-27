from typing import Self, Optional, Iterable
from pymongo import MongoClient
from uuid import UUID
from .schema import Note

NOTE_COLLECTION_NAME = "notes"

class NoteDBClient(MongoClient):
    
    def __init__(self, *args, **kwargs) -> None:
        
        # Initialize super class
        super().__init__(*args, **kwargs)
        
        # Get database and collection
        self._db = self.get_database()
        self._collection = self._db.get_collection(NOTE_COLLECTION_NAME)
    
    @classmethod
    def from_connection_string(cls, connection_string: str) -> Self:
        
        return cls(connection_string)
    
    def insert_note(self, note: Note):
        
        self._collection.insert_one(note.to_document())
        
    def insert_notes(self, notes: Iterable[Note]):
        
        self._collection.insert_many(map(
            lambda note: note.to_document(),
            notes
        ))
        
    def find_note_by_vec_id(self, vec_id: UUID) -> Optional[Note]:
        
        document = self._collection.find_one(
            filter={
                "vec_id": {
                    "$eq": vec_id.hex
                }
            }
        )
        
        if document is None:
            return None
        
        note = Note.from_document(document)
        
        return note
        
    def find_notes_by_vec_ids(self, vec_ids: list[UUID]) -> list[Note]:
        
        notes = []
        for vec_id in vec_ids:
            
            note = self.find_note_by_vec_id(vec_id)
            
            if note is not None:
                notes.append(note)
            
        return notes
    
    def drop_collection(self) -> None:
        
        self.get_database().drop_collection(NOTE_COLLECTION_NAME)
