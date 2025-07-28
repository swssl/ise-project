"""API router modules."""

from .auth import router as auth_router
from .permissions import router as permissions_router
from .users import router as users_router
from .access_logs import router as access_logs_router
from .gateways import router as gateways_router
from .reports import router as reports_router

__all__ = [
    "auth_router",
    "permissions_router",
    "users_router", 
    "access_logs_router",
    "gateways_router",
    "reports_router",
]
