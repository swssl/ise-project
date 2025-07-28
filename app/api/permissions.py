"""Permission management API endpoints."""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status

from ..models import Permission, PermissionCreate, PermissionUpdate, Session
from ..services import PermissionManager
from .auth import get_current_session

router = APIRouter(prefix="/permissions", tags=["permissions"])
permission_manager = PermissionManager()


@router.post("/", response_model=Permission)
async def create_permission(
    permission_data: PermissionCreate,
    current_session: Session = Depends(get_current_session)
):
    """Create a new permission."""
    try:
        permission = permission_manager.create_permission(
            user_id=permission_data.user_id,
            room_id=permission_data.room_id,
            time_slots=permission_data.time_slots
        )
        return permission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create permission: {str(e)}"
        )


@router.get("/user/{user_id}", response_model=List[Permission])
async def get_user_permissions(
    user_id: str,
    current_session: Session = Depends(get_current_session)
):
    """Get all permissions for a specific user."""
    try:
        permissions = permission_manager.get_user_permissions(user_id)
        return permissions
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to retrieve permissions: {str(e)}"
        )


@router.put("/{user_id}/{room_id}", response_model=Permission)
async def update_permission(
    user_id: str,
    room_id: str,
    permission_data: PermissionUpdate,
    current_session: Session = Depends(get_current_session)
):
    """Update an existing permission."""
    try:
        permission = permission_manager.update_permission(
            user_id=user_id,
            room_id=room_id,
            time_slots=permission_data.time_slots
        )
        return permission
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to update permission: {str(e)}"
        )


@router.delete("/{user_id}/{room_id}")
async def revoke_permission(
    user_id: str,
    room_id: str,
    current_session: Session = Depends(get_current_session)
):
    """Revoke a user's permission for a specific room."""
    try:
        permission_manager.revoke_permission(user_id, room_id)
        return {"message": f"Permission revoked for user {user_id} in room {room_id}"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to revoke permission: {str(e)}"
        )


@router.post("/generate-card/{user_id}")
async def generate_card_data(
    user_id: str,
    current_session: Session = Depends(get_current_session)
):
    """Generate card data for a user."""
    try:
        card_data = permission_manager.generate_card_data(user_id)
        return {
            "user_id": user_id,
            "card_data": card_data.hex(),  # Return as hex string
            "message": "Card data generated successfully"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to generate card data: {str(e)}"
        )
