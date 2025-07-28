"""User model."""

from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserRole(Enum):
    """Enumeration for user roles."""
    STUDENT = "student"
    PROFESSOR = "professor"
    STAFF = "staff"
    FACILITY_MANAGER = "facility_manager"


class User(BaseModel):
    """Represents a user in the system."""
    user_id: Optional[str] = None
    email: EmailStr
    full_name: str
    role: UserRole = UserRole.STUDENT
    is_active: bool = True
    created_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    email: EmailStr
    full_name: str
    password: str


class UserUpdate(BaseModel):
    """Schema for updating user information."""
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
