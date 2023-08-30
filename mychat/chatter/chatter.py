from typing import Generator
from .chat_history import ChatHistoryManager
from ..schema import SystemMessage, UserMessage, AssistantMessage
from ..openai_utils import openai_chat
from ..note_manager import NoteManager
from ..notedb import NoteDBClient
from ..vecdb import VecDBClient

def polish_profile(profile: str) -> str:
    
    return (
        "Your name is Natia. "
        "You are NOT an AI!!! "
        "You are merely a human!!! "
        "From now on, "
        "{profile}"
    ).format(
        profile=profile
    )

class Chatter:
    
    def __init__(
            self,
            *,
            profile: str,
            note_manager: NoteManager,
            num_notes_limit: int = 5,
            chat_history_manager: ChatHistoryManager = ChatHistoryManager(),
            do_use_domain_knowledge: bool = False,
            stream: bool = False
        ) -> None:
        
        self._profile = profile
        self._note_manager = note_manager
        self._num_notes_limit = num_notes_limit
        self._chat_history_manager = chat_history_manager
        self._do_use_domain_knowledge = do_use_domain_knowledge
        self._stream = stream
    
    def __call__(self, query: str) -> str | Generator:
        
        # Insert user's query
        self._chat_history_manager.insert_message(
            UserMessage(query)
        )
        
        # Prepare messages
        messages=[
            SystemMessage(polish_profile(self._profile)),
            *self._chat_history_manager.messages
        ]
        
        # Add notes in the prompt if 
        # the domain knowledge is required
        if self.do_use_domain_knowledge:
            messages.append(
                UserMessage(
                    self.include_notes_in_prompt(query)
                )
            )
        
        # Get response from AI
        response = openai_chat(
            messages=messages,
            stream=self._stream
        )
        
        # Insert AI's response
        # only when the stream output is disabled
        if not self._stream:
            self._chat_history_manager.insert_message(
                AssistantMessage(response)
            )
        
        return response
    
    @property
    def profile(self) -> str:
        """Profile of the AI chatter.
        """
        
        return self._profile
    
    @profile.setter
    def profile(self, new_profile: str) -> None:
        self._profile = new_profile
    
    @property
    def do_use_domain_knowledge(self) -> bool:
        return self._do_use_domain_knowledge
    
    @do_use_domain_knowledge.setter
    def do_use_domain_knowledge(self, do_use: bool) -> None:
        self._do_use_domain_knowledge = do_use
    
    @property
    def stream(self) -> bool:
        """Whether the response is stream output.
        """
        
        return self._stream
        
    @property
    def chat_history_manager(self) -> ChatHistoryManager:
        """Chat history manager.
        """
        
        return self._chat_history_manager
    
        
    def include_notes_in_prompt(self, query: str) -> str:
        
        note_contents = self._note_manager.retrieve_similar_note_contents(
            query=query,
            limit=self._num_notes_limit
        )
        
        prompt = (
            "{query} "
            "("
            "Your response MUST be relevant to my query. "
            "Do NOT say anything that is irrelevant!!! "
            "The following notes may be helpful: "
            "{notes}"
            ")"
        ).format(
            query=query,
            notes="\n".join(note_contents)
        )
        
        return prompt
        
        
