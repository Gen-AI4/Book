from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime


class Message(BaseModel):
    """
    Represents a single message in a conversation
    """
    role: str = Field(..., pattern=r"^(user|assistant|system)$")  # "user", "assistant", or "system"
    content: str = Field(..., min_length=1)
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class ChatRequest(BaseModel):
    """
    Request model for chat endpoint
    """
    message: str = Field(..., min_length=1, max_length=10000)
    history: Optional[List[Dict[str, Any]]] = Field(default=None, max_length=50)
    context_window: int = Field(default=5, ge=1, le=20)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)
    max_tokens: int = Field(default=1000, ge=1, le=4000)


class ChatResponse(BaseModel):
    """
    Response model for chat endpoint
    """
    response: str
    context_retrieved: bool = False
    sources: List[str] = Field(default=[])
    timestamp: datetime = Field(default_factory=datetime.utcnow())