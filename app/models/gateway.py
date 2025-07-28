"""Gateway and Message models."""

from typing import Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime
from enum import Enum


# class MessageType(str, Enum):
#     """Types of messages that can be sent to/from gateways."""
#     CARD_UPDATE = "card_update"
#     ACCESS_LOG = "access_log"
#     DEVICE_STATUS = "device_status"
#     SYNC_REQUEST = "sync_request"


class Gateway(BaseModel):
    """Represents a gateway device."""
    gateway_id: str
    name: str
    location: str
    is_online: bool = False
    last_heartbeat: Optional[datetime] = None
    ip_address: Optional[str] = None
    
    class Config:
        from_attributes = True


class DeviceStatus(BaseModel):
    """Represents the status of a device."""
    device_id: str
    is_online: bool
    last_heartbeat: datetime
