"""Access log model."""

from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class AccessLog(BaseModel):
    """Represents an access log entry."""
    log_id: Optional[str] = None
    timestamp: datetime
    user_id: str
    room_id: str
    
    class Config:
        from_attributes = True


class AccessLogCreate(BaseModel):
    """Schema for creating a new access log."""
    user_id: str
    room_id: str
    access_granted: bool = True
    device_id: Optional[str] = None
