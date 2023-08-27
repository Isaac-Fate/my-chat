from typing import Self
from uuid import UUID, uuid4
from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct,
    VectorParams,
    Distance
)

# We will use OpenAI's embedding model
EMBEDDING_DIM = 1536

# Collection of embedding vectors of notes
COLLECTION_NAME = "note-vecs"

class VecDBClient(QdrantClient):
    
    def __init__(self, *args, **kwargs) -> None:
        
        super().__init__(*args, **kwargs)
        
        # Create a new collection if it does not exist
        if COLLECTION_NAME not in self.collection_names:
            self.recreate_collection(
                collection_name=COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=EMBEDDING_DIM,
                    distance=Distance.COSINE
                )
            )
        
        # Get the collection
        self._collection = self.get_collection(COLLECTION_NAME)
    
    @property
    def collection_names(self) -> list[str]:
        
        return list(map(
            lambda collection: collection.name,
            self.get_collections().collections
        ))
    
    @classmethod
    def from_connection_string(cls, connection_string: str) -> Self:
        
        return cls(
            connection_string
        )
    
    def insert_note_vec(self, note_vec: list[float]) -> UUID:
        
        # Get a random UUID
        note_vec_id = uuid4()
        
        # Insert the embedding vector
        self.upsert(
            collection_name=COLLECTION_NAME,
            points=[
                PointStruct(
                    # UUID must be passed as a string
                    id=note_vec_id.hex,
                    vector=note_vec
                )
            ]
        )
        
        return note_vec_id
    
    def retrieve_similar_note_vec_ids(
            self, 
            query_vec: list[float],
            limit: int = 5
        ) -> list[UUID]:
        
        # Find similar points
        points = self.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vec,
            limit=limit,
            with_payload=False
        )
        
        # Vector IDs of similar notes
        vec_ids = list(map(
            lambda point: UUID(point.id),
            points
        ))
        
        return vec_ids
    
    def drop_collection(self) -> None:
        
        # Delete collection
        self.delete_collection(COLLECTION_NAME)
        
        # Recreate the collection
        self.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_DIM,
                distance=Distance.COSINE
            )
        )
