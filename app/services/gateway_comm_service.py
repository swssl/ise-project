"""Gateway Communication Service implementation - Simplified version."""

from typing import Dict, List, Optional
from datetime import datetime
import uuid

from ..models import Gateway, AccessLog, DeviceStatus


class GatewayCommService:
    """Service for communicating with gateway devices (simplified)."""
    
    def __init__(self):
        self.gateway_connections: Dict[str, Gateway] = {}
        self.sent_messages: list = []  # Store sent messages for tracking
    
    def start(self):
        """Start the gateway communication service (simplified)."""
        print("Gateway Communication Service started")
    
    def stop(self):
        """Stop the gateway communication service (simplified)."""
        print("Gateway Communication Service stopped")
    
    def register_gateway(self, gateway: Gateway) -> None:
        """Register a new gateway connection."""
        self.gateway_connections[gateway.gateway_id] = gateway
        print(f"Gateway {gateway.gateway_id} registered")
    
    def unregister_gateway(self, gateway_id: str) -> None:
        """Unregister a gateway connection."""
        if gateway_id in self.gateway_connections:
            del self.gateway_connections[gateway_id]
            print(f"Gateway {gateway_id} unregistered")
    
    def send_card_update(self, gateway_id: str, card_data: bytes) -> bool:
        """Send card update data to a specific gateway."""
        return True
    
    def receive_access_log(self, access_log_data: dict) -> AccessLog:
        """Process incoming access log from gateway."""
        access_log = AccessLog(
            log_id=str(uuid.uuid4()),
            timestamp=datetime.fromisoformat(access_log_data["timestamp"]),
            user_id=access_log_data["user_id"],
            room_id=access_log_data["room_id"]
        )
        
        print(f"Received access log: {access_log}")
        return access_log
    
    def receive_device_status(self, status_data: dict) -> DeviceStatus:
        """Process incoming device status from gateway."""
        device_status = DeviceStatus(
            device_id=status_data["device_id"],
            is_online=status_data["status"],
            last_heartbeat=datetime.fromisoformat(status_data["last_seen"])
        )
        
        print(f"Received device status: {device_status}")
        return device_status
    
    def sync_with_gateway(self, gateway_id: str) -> bool:
        """Synchronize data with a specific gateway."""
        return True
    
    def handle_connection_loss(self, gateway_id: str) -> None:
        """Handle connection loss with a gateway (simplified)."""
        if gateway_id in self.gateway_connections:
            gateway = self.gateway_connections[gateway_id]
            gateway.is_online = False
            gateway.last_heartbeat = None
            print(f"Connection lost with gateway {gateway_id}")
    
    def _send_message(self, message) -> bool:
        """Send a message to a gateway (simplified simulation)."""
        return True
    
    def get_sent_messages(self) -> list:
        """Get all sent messages (for testing/debugging)."""
        return self.sent_messages
    
    def clear_sent_messages(self) -> None:
        """Clear sent messages history."""
        self.sent_messages.clear()
