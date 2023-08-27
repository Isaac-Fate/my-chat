from collections import deque
from ..schema import ChatMessage

BUFFER_SIZE = 16

class ChatHistoryManager:
    
    def __init__(self, buffer_size: int = BUFFER_SIZE) -> None:
        
        self._buffer_size = buffer_size
        self._messages = deque()
    
    @property
    def messages(self) -> list[ChatMessage]:
        
        return list(self._messages)
        
    def insert_message(self, message: ChatMessage):
        
        if len(self._messages) < self._buffer_size:
            self._messages.append(message)
            return
        
        # Remove the earliest message
        self._messages.popleft()
        
        # Insert the latest message
        self._messages.append(message)
    