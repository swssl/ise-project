"""Session Manager service implementation."""

from typing import Dict, Optional
import uuid
from datetime import datetime, timedelta

from ..models import Session, Credentials, User
from ..core.config import settings
from .database import Database


class SessionManager:
    """Service for managing user sessions and authentication."""
    
    def __init__(self, database: Optional[Database] = None):
        self.database = database or Database()
        self.active_sessions: Dict[str, Session] = {}
    
    def create_session(self, credentials: Credentials) -> Optional[Session]:
        """Create a new session after validating credentials."""
        # Validate credentials
        user = self._validate_credentials(credentials)
        if not user or not user.user_id:
            return None
        
        # Create new session
        session_id = str(uuid.uuid4())
        expires_at = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
        
        session = Session(
            session_id=session_id,
            user_id=user.user_id,  # We know this is not None due to the check above
            created_at=datetime.now(),
            expires_at=expires_at,
            is_active=True
        )
        
        # Store in active sessions
        self.active_sessions[session_id] = session
        
        return session
    
    def validate_session(self, session_id: str) -> Optional[Session]:
        """Validate a session and check if it's still active."""
        session = self.active_sessions.get(session_id)
        if not session:
            return None
        
        # Check if session has expired
        if datetime.now() > session.expires_at:
            self.invalidate_session(session_id)
            return None
        
        return session
    
    def invalidate_session(self, session_id: str) -> bool:
        """Invalidate a session (logout)."""
        if session_id in self.active_sessions:
            self.active_sessions[session_id].is_active = False
            del self.active_sessions[session_id]
            return True
        return False
    
    def refresh_session(self, session_id: str) -> Optional[Session]:
        """Refresh a session's expiration time."""
        session = self.validate_session(session_id)
        if not session:
            return None
        
        # Extend expiration time
        session.expires_at = datetime.now() + timedelta(minutes=settings.access_token_expire_minutes)
        self.active_sessions[session_id] = session
        
        return session
    
    def get_user_sessions(self, user_id: str) -> list[Session]:
        """Get all active sessions for a user."""
        return [
            session for session in self.active_sessions.values()
            if session.user_id == user_id and session.is_active
        ]
    
    def invalidate_user_sessions(self, user_id: str) -> int:
        """Invalidate all sessions for a user."""
        sessions_to_remove = []
        for session_id, session in self.active_sessions.items():
            if session.user_id == user_id:
                sessions_to_remove.append(session_id)
        
        for session_id in sessions_to_remove:
            self.invalidate_session(session_id)
        
        return len(sessions_to_remove)
    
    def cleanup_expired_sessions(self) -> int:
        """Remove all expired sessions."""
        current_time = datetime.now()
        expired_sessions = []
        
        for session_id, session in self.active_sessions.items():
            if current_time > session.expires_at:
                expired_sessions.append(session_id)
        
        for session_id in expired_sessions:
            self.invalidate_session(session_id)
        
        return len(expired_sessions)
    
    def _validate_credentials(self, credentials: Credentials) -> Optional[User]:
        """Validate user credentials (simplified for prototype)."""
        # For prototype: Accept any password for existing users
        for user in self.database.get_all_users():
            if user.is_active:
                return user
        return None
    
    def _hash_password(self, password: str) -> str:
        """Hash a password for storage (simplified for prototype)."""
        # In a real implementation, use proper password hashing like bcrypt
        import hashlib
        from ..core.config import settings
        return hashlib.sha256((password + settings.secret_key).encode()).hexdigest()
