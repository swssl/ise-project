"""Database service implementation - In-memory prototype version."""

from typing import List, Optional, Dict, Any
from datetime import datetime

from ..models import User, Permission, AccessLog


class Database:
    """Database service for managing data persistence in memory (prototype)."""
    
    def __init__(self, database_url: Optional[str] = None):
        # In-memory storage
        self.users: Dict[str, User] = {}
        self.permissions: Dict[str, Permission] = {}  # permission_id -> Permission
        self.access_logs: List[AccessLog] = []
        self._initialize_sample_data()
    
    def _initialize_sample_data(self):
        """Initialize with sample data for prototype."""
        # Create sample users
        sample_users = [
            User(
                user_id="1",
                email="admin@th-owl.de",
                full_name="System Administrator",
                is_active=True,
                created_at=datetime.now()
            ),
            User(
                user_id="2", 
                email="alice@th-owl.de",
                full_name="Alice Johnson",
                is_active=True,
                created_at=datetime.now()
            ),
            User(
                user_id="3",
                email="bob@th-owl.de",
                full_name="Bob Smith",
                is_active=True,
                created_at=datetime.now()
            )
        ]
        
        for user in sample_users:
            self.users[user.user_id] = user
    
    def save_user(self, user: User) -> None:
        """Save a user to in-memory storage."""
        if user.user_id:
            self.users[user.user_id] = user
    
    def save_access_log(self, log: AccessLog) -> None:
        """Save an access log entry to in-memory storage."""
        if not log.log_id:
            log.log_id = f"log_{len(self.access_logs) + 1}"
        self.access_logs.append(log)
    
    def get_permissions(self, user_id: str) -> List[Permission]:
        """Get all permissions for a specific user."""
        return [
            permission for permission in self.permissions.values()
            if permission.user_id == user_id
        ]
    
    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Get a user by their ID."""
        return self.users.get(user_id)
    
    def save_permission(self, permission: Permission) -> None:
        """Save a permission to in-memory storage."""
        if permission.permission_id:
            self.permissions[permission.permission_id] = permission
    
    def delete_permission(self, user_id: str, room_id: str) -> None:
        """Delete a permission by setting it as inactive."""
        for permission in self.permissions.values():
            if (permission.user_id == user_id and 
                permission.room_id == room_id and 
                permission.is_active):
                permission.is_active = False
                break
    
    def get_access_logs(self, 
                       user_id: Optional[str] = None,
                       room_id: Optional[str] = None,
                       limit: int = 100) -> List[AccessLog]:
        """Get access logs with optional filters."""
        filtered_logs = self.access_logs
        
        if user_id:
            filtered_logs = [log for log in filtered_logs if log.user_id == user_id]
        
        if room_id:
            filtered_logs = [log for log in filtered_logs if log.room_id == room_id]
        
        # Return most recent first, limited
        return sorted(filtered_logs, key=lambda x: x.timestamp, reverse=True)[:limit]
    
    def get_all_users(self) -> List[User]:
        """Get all users."""
        return list(self.users.values())
