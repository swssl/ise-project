"""User management API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..models import User, UserCreate, UserUpdate, Session
from ..services import Database
from .auth import get_current_session

router = APIRouter(prefix="/users", tags=["users"])
database = Database()


@router.post("/", response_model=User)
async def create_user(
    user_data: UserCreate,
    current_session: Session = Depends(get_current_session)
):
    """Create a new user."""
    try:
        import uuid
        from datetime import datetime
        
        user = User(
            user_id=str(uuid.uuid4()),
            email=user_data.email,
            full_name=user_data.full_name,
            is_active=True,
            created_at=datetime.now()
        )
        
        database.save_user(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create user: {str(e)}"
        )


@router.get("/{user_id}", response_model=User)
async def get_user(
    user_id: str,
    current_session: Session = Depends(get_current_session)
):
    """Get a user by ID."""
    user = database.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put("/{user_id}", response_model=User)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_session: Session = Depends(get_current_session)
):
    """Update user information."""
    user = database.get_user_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # Update user fields
    if user_data.email is not None:
        user.email = user_data.email
    if user_data.full_name is not None:
        user.full_name = user_data.full_name
    if user_data.is_active is not None:
        user.is_active = user_data.is_active
    
    try:
        database.save_user(user)
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update user: {str(e)}"
        )
