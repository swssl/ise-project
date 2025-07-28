"""Authentication API endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from ..models import Credentials, Session, Token
from ..services import SessionManager

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()
session_manager = SessionManager()


@router.post("/login", response_model=Token)
async def login(credentials: Credentials):
    """Authenticate user and create session."""
    session = session_manager.create_session(credentials)
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(
        access_token=session.session_id,
        token_type="bearer",
        expires_in=1800  # 30 minutes
    )


@router.post("/logout")
async def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Logout user and invalidate session."""
    session_id = credentials.credentials
    success = session_manager.invalidate_session(session_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Session not found"
        )
    
    return {"message": "Successfully logged out"}


@router.post("/refresh", response_model=Token)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Refresh authentication token."""
    session_id = credentials.credentials
    session = session_manager.refresh_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return Token(
        access_token=session.session_id,
        token_type="bearer",
        expires_in=1800
    )


@router.get("/me", response_model=Session)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """Get current user session information."""
    session_id = credentials.credentials
    session = session_manager.validate_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return session


# Dependency to get current session
async def get_current_session(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Session:
    """Dependency to validate and get current session."""
    session_id = credentials.credentials
    session = session_manager.validate_session(session_id)
    
    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return session
