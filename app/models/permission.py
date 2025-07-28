"""Permission and TimeSlot models."""

from typing import List, Optional
from pydantic import BaseModel
from datetime import time


class TimeSlot(BaseModel):
    """Represents a time slot for access permissions."""
    start_time: time
    end_time: time
    day_of_week: str
    is_active: bool = True


class Permission(BaseModel):
    """Represents a user's permission to access a specific room."""
    permission_id: Optional[str] = None
    user_id: str
    room_id: str
    time_slots: List[TimeSlot]
    # is_active: bool = True
    
    class Config:
        from_attributes = True


class PermissionCreate(BaseModel):
    """Schema for creating a new permission."""
    user_id: str
    room_id: str
    time_slots: List[TimeSlot]


class PermissionUpdate(BaseModel):
    """Schema for updating an existing permission."""
    time_slots: List[TimeSlot]
