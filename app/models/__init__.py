"""Data models for the smart lock system."""

from .permission import Permission, TimeSlot, PermissionCreate, PermissionUpdate
from .access_log import AccessLog, AccessLogCreate
from .user import User, UserCreate, UserUpdate
from .gateway import Gateway, DeviceStatus
from .session import Session, Credentials, Token
from .report import Report, ReportRequest, ReportType

__all__ = [
    "Permission",
    "TimeSlot",
    "PermissionCreate",
    "PermissionUpdate",
    "AccessLog",
    "AccessLogCreate",
    "User",
    "UserCreate", 
    "UserUpdate",
    "Gateway",
    "DeviceStatus",
    "Session",
    "Credentials",
    "Token",
    "Report",
    "ReportRequest",
    "ReportType",
]
