"""Session and authentication models."""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class Credentials(BaseModel):
    """User login credentials."""
    username: str
    password: str


class Session(BaseModel):
    """User session information."""
    session_id: str
    user_id: str
    created_at: datetime
    expires_at: datetime
    is_active: bool = True
    
    class Config:
        from_attributes = True


class Token(BaseModel):
    """Authentication token response."""
    access_token: str
    token_type: str = "bearer"
    expires_in: int
