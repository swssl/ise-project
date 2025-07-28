"""Permission Manager service implementation."""

from typing import List
import uuid
from datetime import datetime

from ..models import Permission, PermissionCreate, PermissionUpdate, TimeSlot
from .database import Database


class PermissionManager:
    """Service for managing user permissions."""
    
    def __init__(self, database: Database = None):
        self.database = database or Database()
        self.active_permissions: List[Permission] = []
    
    def create_permission(self, user_id: str, room_id: str, time_slots: List[TimeSlot]) -> Permission:
        """Create a new permission for a user."""
        permission = Permission(
            permission_id=str(uuid.uuid4()),
            user_id=user_id,
            room_id=room_id,
            time_slots=time_slots,
            is_active=True
        )
        
        # Save to database
        self.database.save_permission(permission)
        
        # Update active permissions cache
        self._refresh_active_permissions()
        
        # Schedule card update
        self.schedule_card_update(f"card_{user_id}")
        
        return permission
    
    def revoke_permission(self, user_id: str, room_id: str) -> None:
        """Revoke a user's permission for a specific room."""
        # Mark permission as inactive in database
        self.database.delete_permission(user_id, room_id)
        
        # Update active permissions cache
        self._refresh_active_permissions()
        
        # Schedule card update
        self.schedule_card_update(f"card_{user_id}")
    
    def update_permission(self, user_id: str, room_id: str, time_slots: List[TimeSlot]) -> Permission:
        """Update an existing permission."""
        # First revoke the old permission
        self.revoke_permission(user_id, room_id)
        
        # Then create a new one with updated time slots
        return self.create_permission(user_id, room_id, time_slots)
    
    def generate_card_data(self, user_id: str) -> bytes:
        """Generate card data for a user based on their permissions."""
        user_permissions = self.database.get_permissions(user_id)
        
        # Create a simple card data structure
        # In a real implementation, this would be more sophisticated
        card_data = {
            "user_id": user_id,
            "permissions": [],
            "generated_at": datetime.now().isoformat()
        }
        
        for permission in user_permissions:
            card_data["permissions"].append({
                "room_id": permission.room_id,
                "time_slots": [
                    {
                        "start_time": ts.start_time.isoformat(),
                        "end_time": ts.end_time.isoformat(),
                        "day_of_week": ts.day_of_week
                        
                    }
                    for ts in permission.time_slots
                ]
            })
        
        # Convert to bytes (in real implementation, this might be encrypted)
        import json
        return json.dumps(card_data).encode('utf-8')
    
    def schedule_card_update(self, card_id: str) -> None:
        """Schedule a card update to be sent to the gateway."""
        # In a real implementation, this would add the update to a queue
        # or send it directly to the GatewayCommService
        print(f"Scheduled card update for card_id: {card_id}")
        # TODO: Integrate with GatewayCommService to send actual update
    
    def get_user_permissions(self, user_id: str) -> List[Permission]:
        """Get all active permissions for a user."""
        return self.database.get_permissions(user_id)
    
    def _refresh_active_permissions(self) -> None:
        """Refresh the active permissions cache."""
        # In a real implementation, this might load all active permissions
        # For now, we'll keep it simple
        pass
