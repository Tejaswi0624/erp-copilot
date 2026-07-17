from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class MessageBase(BaseModel):
    role: str
    content: str


class MessageOut(MessageBase):
    id: int
    conversation_id: int
    tokens_used: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationBase(BaseModel):
    title: Optional[str] = None
    module_context: Optional[str] = None


class ConversationCreate(ConversationBase):
    pass


class ConversationOut(ConversationBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None
    messages: List[MessageOut] = []

    model_config = {"from_attributes": True}


class ConversationSummary(BaseModel):
    id: int
    title: Optional[str] = None
    module_context: Optional[str] = None
    created_at: datetime
    message_count: int = 0

    model_config = {"from_attributes": True}


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None
    module_context: Optional[str] = None


class ChatResponse(BaseModel):
    conversation_id: int
    message: MessageOut
    reply: MessageOut
