from dataclasses import dataclass
from typing import List, Optional

@dataclass
class BaseMessage:
    """Base class for chat messages."""
    role: str
    content: str

@dataclass
class UserMessage(BaseMessage):
    """Class representing a user message."""
    def __init__(self, content: str):
        super().__init__(role="user", content=content)

@dataclass
class AssistantMessage(BaseMessage):
    """Class representing an assistant message."""
    def __init__(self, content: str):
        super().__init__(role="assistant", content=content)

@dataclass
class Messages:
    """Class for managing a collection of chat messages."""
    messages: List[BaseMessage] = None

    def __init__(self):
        self.messages = []

    def add_user_message(self, content: str) -> None:
        """Add a user message to the collection."""
        self.messages.append(UserMessage(content))

    def add_assistant_message(self, content: str) -> None:
        """Add an assistant message to the collection."""
        self.messages.append(AssistantMessage(content))

    def to_dict(self) -> List[dict]:
        """Convert messages to a list of dictionaries."""
        return [{"role": msg.role, "content": msg.content} for msg in self.messages] 