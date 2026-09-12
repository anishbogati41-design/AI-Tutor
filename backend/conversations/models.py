from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True, slots=True)
class MessageRecord:
    id: int
    conversation_id: int
    role: str
    content: str
    created_at: datetime


@dataclass(frozen=True, slots=True)
class ConversationRecord:
    id: int
    user_id: int
    title: str
    created_at: datetime
    updated_at: datetime
    messages: tuple[MessageRecord, ...] = ()
